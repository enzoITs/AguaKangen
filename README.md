# Água Kangen — site

Site estático (HTML, CSS e JavaScript puros, sem build de dependências).

## Estrutura

| Arquivo | Função |
| --- | --- |
| `index.html` | Página inicial: hero, tecnologia, tipos de água, produtos, Enagic, demonstração, suporte, FAQ e CTA final. |
| `produtos/<slug>/index.html` | Páginas de produto **geradas** a partir de `produtos.json`. Não edite à mão. |
| `produtos.json` | Fonte de dados dos produtos e do domínio do site (`site.baseUrl`). |
| `gerar_paginas.py` | Gera as páginas de produto, o `sitemap.xml` e o `robots.txt`. |
| `style.css` | Sistema visual completo (tokens de cor, tipografia, espaçamento, componentes). |
| `script.js` | WhatsApp, abas de tipo de água, galeria, menu mobile, animações de entrada. |
| `img/` | Imagens em `.webp` (as originais `.png`/`.jpg` continuam na pasta como backup). |
| `referencia/` | Referências visuais. Bloqueada no `robots.txt` e não publicada. |

## Antes de publicar

1. **Domínio.** Troque `https://SEU-DOMINIO.com.br` em `produtos.json` (campo `site.baseUrl`) e em `index.html` (canonical, Open Graph e JSON-LD).
2. Rode `python3 gerar_paginas.py` para regerar páginas de produto, `sitemap.xml` e `robots.txt` com o domínio novo.
3. **WhatsApp.** O número fica em `script.js`, na constante `CONSULTOR.whatsapp` (DDI + DDD + número, só dígitos).

## Medição de conversão

Cada CTA tem `data-event` (`cta_demo_hero`, `cta_whatsapp_product`, `cta_demo_final`, …) e, nos produtos, `data-produto`. No clique, o evento é enviado para `window.dataLayer` e para `gtag`, quando existirem. Basta instalar o GTM ou o GA4 no `<head>` — nenhum outro código é necessário.

## Conteúdo que ainda falta

- Cidade e região atendidas (hoje o site não nomeia nenhuma localidade, o que impede ranquear para buscas locais).
- Endereço, telefone e horário para o Google Meu Negócio e para o schema `LocalBusiness`.
- Depoimentos reais de clientes e fotos das demonstrações.
