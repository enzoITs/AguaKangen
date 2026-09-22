#!/usr/bin/env python3
"""Gera as páginas de produto, o sitemap.xml e o robots.txt a partir de produtos.json.

Uso: python3 gerar_paginas.py
Rode de novo sempre que editar produtos.json ou trocar o domínio em site.baseUrl.
"""
import json
from datetime import date
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DADOS = json.loads((RAIZ / "produtos.json").read_text(encoding="utf-8"))
SITE = DADOS["site"]
PRODUTOS = DADOS["produtos"]
BASE = SITE["baseUrl"].rstrip("/")

GOTA = '<svg viewBox="0 0 24 24"><path d="M12 3.5c3.4 4 6 7.3 6 10.4a6 6 0 0 1-12 0c0-3.1 2.6-6.4 6-10.4Z"/></svg>'
WHATSAPP_ICONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.7a8.2 8.2 0 0 1-12 7.3L3 21l2-5.3a8.2 8.2 0 1 1 15.5-4Zm-4.8 2.2c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.6.1-.2.3-.6.8-.8 1-.1.2-.3.2-.5.1-1.5-.7-2.5-1.8-3.1-3.2-.1-.2 0-.4.1-.5l.4-.5c.1-.2.1-.3 0-.5L9.9 8c-.1-.3-.3-.3-.5-.3h-.5c-.2 0-.5.1-.7.4-.3.3-.9.9-.9 2.2 0 1.3.9 2.5 1.1 2.7.1.2 1.8 2.8 4.4 3.9.6.3 1.1.4 1.5.5.6.2 1.1.1 1.5.1.5-.1 1.4-.6 1.6-1.2.2-.6.2-1.1.1-1.2-.1-.2-.3-.2-.5-.3Z"/></svg>'


def e(texto):
    return escape(str(texto), quote=True)


def cta(classe, evento, produto, mensagem, rotulo):
    return (
        f'<a class="{classe} js-whatsapp" href="#agendar" data-event="{evento}" '
        f'data-produto="{e(produto)}" data-message="{e(mensagem)}">{rotulo} <span aria-hidden="true">→</span></a>'
    )


def json_ld(produto, url):
    grafo = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "name": produto["nome"],
                "description": produto["resumo"],
                "image": [f"{BASE}/{img}.webp" for img in produto["galeria"]],
                "brand": {"@type": "Brand", "name": "Enagic"},
                "category": produto["categoria"],
                "url": url,
                "areaServed": ["Marília, SP", "Bauru, SP", "Região de Marília e Bauru"],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Produtos", "item": f"{BASE}/#produtos"},
                    {"@type": "ListItem", "position": 3, "name": produto["nome"], "item": url},
                ],
            },
        ],
    }
    return json.dumps(grafo, ensure_ascii=False, indent=2)


def pagina(produto):
    slug = produto["slug"]
    nome = produto["nome"]
    url = f"{BASE}/produtos/{slug}/"
    titulo = f"{nome} | Kangen Enagic em Marília e Bauru"
    descricao = f"{produto['resumo']} Agende uma demonstração gratuita na sua casa em Marília, Bauru e região."
    capa = produto["imagem"]
    o_a = "a" if nome.startswith("Ducha") else "o"
    do_da = "da" if o_a == "a" else "do"
    msg_demo = f"Olá! Conheci {o_a} {nome} pelo site e gostaria de agendar uma demonstração."
    msg_vendedor = f"Olá! Conheci {o_a} {nome} pelo site e gostaria de saber mais."

    galeria = ""
    if len(produto["galeria"]) > 1:
        botoes = "\n".join(
            f'            <button type="button" class="gallery-thumb{" is-active" if i == 0 else ""}" data-src="../../{img}.webp" aria-label="Ver imagem {i + 1} {do_da} {e(nome)}"><img src="../../{img}.webp" alt="" width="84" height="68" loading="lazy" decoding="async"></button>'
            for i, img in enumerate(produto["galeria"])
        )
        galeria = f'\n          <div class="gallery">\n{botoes}\n          </div>'

    diferenciais = "\n".join(
        f'          <article class="feature-card reveal"><h3>{e(d["titulo"])}</h3><p>{e(d["texto"])}</p></article>'
        for d in produto["diferenciais"]
    )
    publico = "\n".join(f"          <li>{e(p)}</li>" for p in produto["paraQuem"])
    specs = "\n".join(
        f'              <tr><th scope="row">{e(rotulo)}</th><td>{e(valor)}</td></tr>' for rotulo, valor in produto["specs"]
    )
    outros = "\n".join(
        f'''          <a class="other-card" href="../{o["slug"]}/">
            <img src="../../{o["imagem"]}.webp" alt="" width="92" height="92" loading="lazy" decoding="async">
            <div><h3>{e(o["nome"])}</h3><p>{e(o["posicionamento"])}</p></div>
          </a>'''
        for o in PRODUTOS
        if o["slug"] != slug
    )
    rodape_produtos = "\n".join(
        f'            <li><a href="../{o["slug"]}/">{e(o["nome"])}</a></li>' for o in PRODUTOS
    )

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titulo)}</title>
  <meta name="description" content="{e(descricao)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0D4C5C">

  <meta property="og:type" content="product">
  <meta property="og:site_name" content="{e(SITE["nome"])}">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(titulo)}">
  <meta property="og:description" content="{e(descricao)}">
  <meta property="og:image" content="{BASE}/{capa}.webp">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(titulo)}">
  <meta name="twitter:description" content="{e(descricao)}">
  <meta name="twitter:image" content="{BASE}/{capa}.webp">

  <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../../img/apple-touch-icon.png">
  <link rel="preload" as="image" href="../../{capa}.webp" fetchpriority="high">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../style.css">
  <script type="application/ld+json">
{json_ld(produto, url)}
  </script>
</head>
<body>
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

  <header class="site-header">
    <div class="container nav">
      <a class="logo" href="../../" aria-label="Água Kangen, início">
        <span class="logo-mark" aria-hidden="true">{GOTA}</span>
        <span>Água <strong>Kangen</strong></span>
      </a>
      <button class="mobile-nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
      <nav class="desktop-nav" id="main-nav" aria-label="Navegação principal">
        <a href="../../#tecnologia">Tecnologia</a>
        <a href="../../#produtos">Produtos</a>
        <a href="../../#demonstracao">Demonstração</a>
        <a href="../../#perguntas">Perguntas</a>
        <a href="#agendar">Contato</a>
      </nav>
      {cta("header-cta", "cta_demo_header", nome, msg_demo, "Agendar demonstração").replace('→', '↗')}
    </div>
    <div class="ph-rule" aria-hidden="true"></div>
  </header>

  <main id="conteudo">
    <nav class="breadcrumb container" aria-label="Você está em">
      <ol>
        <li><a href="../../">Início</a></li>
        <li><a href="../../#produtos">Produtos</a></li>
        <li><span aria-current="page">{e(nome)}</span></li>
      </ol>
    </nav>

    <section class="container product-hero" aria-labelledby="produto-titulo">
      <div>
        <figure class="product-media">
          <img id="gallery-main" src="../../{capa}.webp" alt="{e(nome)}, {e(produto["categoria"].lower())} Kangen da Enagic" fetchpriority="high" decoding="async">
          <span class="product-tag">{e(produto["badge"])}</span>
        </figure>{galeria}
      </div>
      <div class="product-body">
        <p class="product-kicker">{e(produto["categoria"])} · Enagic®</p>
        <h1 id="produto-titulo">{e(nome)}</h1>
        <p class="lead">{e(produto["chamada"])} {e(produto["resumo"])}</p>
        <div class="product-actions">
          {cta("button button-primary", "cta_demo_product", nome, msg_demo, "Agendar demonstração")}
          {cta("button button-ghost", "cta_whatsapp_product", nome, msg_vendedor, "Falar com o vendedor")}
        </div>
      </div>
    </section>

    <section class="section-tight" aria-labelledby="diferenciais-titulo">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Diferenciais</p>
          <h2 id="diferenciais-titulo">{e(produto["posicionamento"])}</h2>
        </div>
        <div class="feature-grid">
{diferenciais}
        </div>
      </div>
    </section>

    <section class="section-tight" aria-labelledby="publico-titulo">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Para quem faz sentido</p>
          <h2 id="publico-titulo">Um bom ponto de partida se você se identifica com algum destes perfis.</h2>
        </div>
        <ul class="audience">
{publico}
        </ul>
      </div>
    </section>

    <section class="section-tight" aria-labelledby="specs-titulo">
      <div class="container split">
        <p class="eyebrow reveal">Ficha técnica</p>
        <div class="reveal delay-1">
          <h2 id="specs-titulo">Especificações {do_da} {e(nome)}</h2>
          <p class="lead">{e(produto["descricao"])}</p>
          <table class="spec-table">
            <caption class="visually-hidden">Especificações técnicas {do_da} {e(nome)}</caption>
            <tbody>
{specs}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="cta-final" id="agendar" aria-labelledby="cta-titulo">
      <div class="container">
        <div class="cta-panel on-dark reveal">
          <div>
            <p class="eyebrow">Demonstração sem compromisso</p>
            <h2 id="cta-titulo">Veja {o_a} {e(nome)} funcionando antes de decidir.</h2>
            <p class="lead">Todo o atendimento é feito pelo WhatsApp. Chame no botão ao lado e uma pessoa confirma a disponibilidade para a sua cidade em Marília, Bauru e região.</p>
          </div>
          <div class="cta-actions">
            {cta("button button-primary", "cta_demo_final", nome, msg_demo, "Agendar demonstração")}
            {cta("button button-ghost", "cta_whatsapp_final", nome, msg_vendedor, "Falar com o vendedor")}
            <small>Você será direcionado ao WhatsApp com a mensagem já pronta.</small>
          </div>
        </div>
      </div>
    </section>

    <section class="section-tight flush-top" aria-labelledby="outros-titulo">
      <div class="container">
        <p class="eyebrow">Outros equipamentos</p>
        <h2 id="outros-titulo" class="visually-hidden">Outros equipamentos</h2>
        <div class="other-products">
{outros}
        </div>
      </div>
    </section>

    <section class="disclaimer-band" aria-label="Aviso">
      <div class="container">
        <strong>Informação responsável</strong>
        <p>Nossos produtos não se destinam a diagnosticar, tratar, curar ou prevenir qualquer doença.</p>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="logo" href="../../">
            <span class="logo-mark" aria-hidden="true">{GOTA}</span>
            <span>Água <strong>Kangen</strong></span>
          </a>
          <p>Distribuidor independente Enagic®. Demonstração presencial gratuita dos ionizadores de água Kangen em Marília, Bauru e região.</p>
        </div>
        <nav class="footer-col" aria-label="Seções">
          <h2>Navegação</h2>
          <ul>
            <li><a href="../../#tecnologia">Tecnologia</a></li>
            <li><a href="../../#tipos">Tipos de água</a></li>
            <li><a href="../../#demonstracao">Demonstração</a></li>
            <li><a href="../../#perguntas">Perguntas frequentes</a></li>
          </ul>
        </nav>
        <nav class="footer-col" aria-label="Produtos">
          <h2>Produtos</h2>
          <ul>
{rodape_produtos}
          </ul>
        </nav>
        <div class="footer-col">
          <h2>Contato</h2>
          <ul>
            <li>{cta("cfg-telefone", "cta_whatsapp_footer", nome, msg_vendedor, "Falar no WhatsApp").replace(' <span aria-hidden="true">→</span>', '')}</li>
            <li><a href="https://kangensaude.com.br/" target="_blank" rel="noopener">Site institucional</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>Distribuidor independente Enagic®. Este site tem caráter informativo e comercial. O equipamento realiza tratamento e filtragem de água; não possui indicação para diagnóstico, tratamento, cura ou prevenção de doenças.</p>
        <p>© <span class="js-year">{date.today().year}</span> Água Kangen</p>
      </div>
    </div>
  </footer>

  <a class="whatsapp-float js-whatsapp" href="#agendar" data-event="cta_whatsapp_float" data-produto="{e(nome)}" data-message="{e(msg_vendedor)}" aria-label="Falar pelo WhatsApp">
    {WHATSAPP_ICONE}
  </a>

  <div class="mobile-bar">
    {cta("button button-primary", "cta_demo_mobilebar", nome, msg_demo, "Agendar demonstração")}
  </div>

  <script src="../../script.js" defer></script>
</body>
</html>
"""


def main():
    hoje = date.today().isoformat()
    urls = [f"{BASE}/"]
    for produto in PRODUTOS:
        destino = RAIZ / "produtos" / produto["slug"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(produto), encoding="utf-8")
        urls.append(f"{BASE}/produtos/{produto['slug']}/")
        print(f"gerado {destino.relative_to(RAIZ)}")

    entradas = "\n".join(f"  <url><loc>{u}</loc><lastmod>{hoje}</lastmod></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entradas}\n</urlset>\n',
        encoding="utf-8",
    )
    (RAIZ / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nDisallow: /referencia/\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8"
    )
    print("gerado sitemap.xml e robots.txt")


if __name__ == "__main__":
    main()
