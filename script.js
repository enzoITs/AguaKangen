/* ============================================================
   Água Kangen — script único do site
   CONFIGURE AQUI ANTES DE PUBLICAR.
   whatsapp: DDI + DDD + número, só dígitos. Ex: 5511999998888
   ============================================================ */
const CONSULTOR = {
  whatsapp: '5514996478302',
  telefoneExibicao: 'Falar no WhatsApp'
};

document.addEventListener('DOMContentLoaded', () => {
  if (CONSULTOR.whatsapp === '5500000000000') {
    console.warn('AVISO: número de WhatsApp não configurado em CONSULTOR.whatsapp.');
  }

  document.querySelectorAll('.cfg-telefone').forEach((element) => {
    element.textContent = CONSULTOR.telefoneExibicao;
  });

  document.querySelectorAll('.js-year').forEach((element) => {
    element.textContent = new Date().getFullYear();
  });

  initWhatsAppLinks();
  initWaterTabs();
  initRevealAnimations();
  initMobileNav();
  initStickyHeader();
  initGallery();
});

/* ---------- WhatsApp + medição de origem ---------- */

function createWhatsAppLink(message) {
  return `https://wa.me/${CONSULTOR.whatsapp}?text=${encodeURIComponent(message)}`;
}

/**
 * Cada CTA carrega data-message (texto enviado) e data-event (nome do evento).
 * O clique é empurrado para o dataLayer e para o gtag, quando existirem, sem
 * adicionar nenhuma ferramenta de tracking ao site.
 */
function initWhatsAppLinks() {
  document.querySelectorAll('.js-whatsapp').forEach((link) => {
    const message = link.dataset.message || 'Olá! Gostaria de saber mais sobre a demonstração presencial.';
    link.href = createWhatsAppLink(message);
    link.target = '_blank';
    link.rel = 'noopener';

    link.addEventListener('click', () => {
      const event = link.dataset.event || 'cta_whatsapp';
      const produto = link.dataset.produto || '';

      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event, produto });

      if (typeof window.gtag === 'function') {
        window.gtag('event', event, { produto });
      }
    });
  });
}

/* ---------- Tipos de água ---------- */

function initWaterTabs() {
  const tabs = document.querySelectorAll('.water-tab');
  const panel = document.getElementById('water-panel');
  if (!tabs.length || !panel) return;

  const data = {
    kangen: {
      ph: '8.5–9.5',
      use: 'Uso para consumo',
      title: 'Água Kangen',
      description: 'Indicada para beber e preparar alimentos, como café, chá e receitas do dia a dia.',
      list: ['Consumo diário', 'Cozinhar e preparar bebidas', 'Uso doméstico na cozinha'],
      color: '#E7F7F7'
    },
    neutral: {
      ph: '7.0',
      use: 'Uso geral',
      title: 'Água Neutra',
      description: 'Água filtrada em faixa de pH neutra para usos gerais, como preparo de alimentos e uso com medicamentos conforme orientação profissional.',
      list: ['Preparo de alimentos', 'Uso geral na cozinha', 'Uso com medicamentos conforme orientação'],
      color: '#F1F8F8'
    },
    beauty: {
      ph: '6.0',
      use: 'Uso externo · não ingerir',
      title: 'Água de Beleza',
      description: 'Opção de pH levemente ácido indicada para cuidados externos, como pele e cabelo.',
      list: ['Cuidados externos com a pele', 'Enxágue de cabelo', 'Não indicada para ingestão'],
      color: '#F6EBD8'
    },
    acid: {
      ph: '2.5',
      use: 'Uso externo · não ingerir',
      title: 'Água Super Ácida',
      description: 'Opção destinada à assepsia e limpeza de superfícies e utensílios domésticos.',
      list: ['Assepsia de superfícies', 'Limpeza de utensílios', 'Não indicada para ingestão'],
      color: '#F7E0D6'
    },
    alkaline: {
      ph: '11.5',
      use: 'Uso externo · não ingerir',
      title: 'Água Super Alcalina',
      description: 'Opção para limpeza pesada e remoção de resíduos em tarefas domésticas.',
      list: ['Limpeza pesada', 'Remoção de resíduos', 'Não indicada para ingestão'],
      color: '#E6E2F2'
    }
  };

  tabs.forEach((tab) => tab.addEventListener('click', () => {
    const item = data[tab.dataset.water];
    if (!item) return;

    tabs.forEach((button) => {
      button.classList.remove('active');
      button.setAttribute('aria-selected', 'false');
    });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');

    panel.classList.add('changing');
    window.setTimeout(() => {
      document.getElementById('water-ph').textContent = item.ph;
      document.getElementById('water-use').textContent = item.use;
      document.getElementById('water-title').textContent = item.title;
      document.getElementById('water-description').textContent = item.description;
      document.querySelector('.water-meter').style.background = item.color;
      document.getElementById('water-list').innerHTML = item.list
        .map((entry) => `<li>${entry}</li>`)
        .join('');
      panel.classList.remove('changing');
    }, 170);
  }));
}

/* ---------- Animações de entrada ---------- */

function initRevealAnimations() {
  const elements = document.querySelectorAll('.reveal');
  if (!elements.length) return;

  const semAnimacao = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    || !('IntersectionObserver' in window);

  if (semAnimacao) {
    elements.forEach((element) => element.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  elements.forEach((element) => observer.observe(element));
}

/* ---------- Navegação mobile ---------- */

function initMobileNav() {
  const toggle = document.querySelector('.mobile-nav-toggle');
  const nav = document.getElementById('main-nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && nav.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
}

/* ---------- Cabeçalho ao rolar ---------- */

function initStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const update = () => header.classList.toggle('is-stuck', window.scrollY > 12);
  update();
  window.addEventListener('scroll', update, { passive: true });
}

/* ---------- Galeria da página de produto ---------- */

function initGallery() {
  const main = document.getElementById('gallery-main');
  const thumbs = document.querySelectorAll('.gallery-thumb');
  if (!main || !thumbs.length) return;

  thumbs.forEach((thumb) => thumb.addEventListener('click', () => {
    main.src = thumb.dataset.src;
    thumbs.forEach((item) => item.classList.toggle('is-active', item === thumb));
  }));
}
