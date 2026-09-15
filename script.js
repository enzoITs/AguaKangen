/*
  CONFIGURE AQUI antes de publicar.
  O número deve conter DDI + DDD + número, apenas dígitos.
*/
const CONSULTOR = {
  nome: 'Seu nome',
  cidade: 'sua cidade',
  whatsapp: '5500000000000',
  telefoneExibicao: 'Falar no WhatsApp'
};

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.cfg-nome').forEach((element) => {
    element.textContent = CONSULTOR.nome;
  });

  document.querySelectorAll('.cfg-cidade').forEach((element) => {
    element.textContent = CONSULTOR.cidade;
  });

  document.querySelectorAll('.cfg-telefone').forEach((element) => {
    element.textContent = CONSULTOR.telefoneExibicao;
  });

  document.querySelectorAll('.js-whatsapp').forEach((link) => {
    const message = link.dataset.message || 'Olá! Gostaria de saber mais sobre a demonstração presencial.';
    link.href = createWhatsAppLink(message);
    link.target = '_blank';
    link.rel = 'noopener';
  });

  const phoneInput = document.getElementById('whats');
  phoneInput.addEventListener('input', () => {
    const digits = phoneInput.value.replace(/\D/g, '').slice(0, 11);
    phoneInput.value = digits.replace(/^(\d{0,2})(\d{0,5})(\d{0,4}).*/, (_, ddd, first, last) => {
      if (!first) return ddd;
      return `(${ddd}) ${first}${last ? `-${last}` : ''}`;
    });
  });

  document.getElementById('lead-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const nome = document.getElementById('nome').value.trim();
    const whats = phoneInput.value.trim();
    const bairro = document.getElementById('bairro').value.trim();
    const message = `Olá! Meu nome é ${nome}. Gostaria de agendar uma demonstração presencial. Meu WhatsApp é ${whats} e moro em ${bairro}.`;
    window.open(createWhatsAppLink(message), '_blank', 'noopener');
  });

  initWaterTabs();
  initDemoCarousel();
  initRevealAnimations();
});

function createWhatsAppLink(message) {
  return `https://wa.me/${CONSULTOR.whatsapp}?text=${encodeURIComponent(message)}`;
}

function initWaterTabs() {
  const data = {
    kangen: { ph: '8.5–9.5', use: 'Uso para consumo', title: 'Água Kangen', description: 'Indicada para beber e preparar alimentos, como café, chá e receitas do dia a dia.', list: ['Consumo diário', 'Cozinhar e preparar bebidas', 'Uso doméstico na cozinha'], color: '#7FDBFF' },
    neutral: { ph: '7.0', use: 'Uso geral', title: 'Água Neutra', description: 'Água filtrada em faixa de pH neutra para usos gerais, como preparo de alimentos e uso com medicamentos conforme orientação profissional.', list: ['Preparo de alimentos', 'Uso geral na cozinha', 'Uso com medicamentos conforme orientação'], color: '#F4F8FB' },
    beauty: { ph: '6.0', use: 'Uso externo · não ingerir', title: 'Água de Beleza', description: 'Opção de pH levemente ácido indicada para cuidados externos, como pele e cabelo.', list: ['Cuidados externos com a pele', 'Enxágue de cabelo', 'Não indicada para ingestão'], color: '#DCEFF9' },
    acid: { ph: '2.5', use: 'Uso externo · não ingerir', title: 'Água Super Ácida', description: 'Opção destinada à assepsia e limpeza de superfícies e utensílios domésticos.', list: ['Assepsia de superfícies', 'Limpeza de utensílios', 'Não indicada para ingestão'], color: '#D3E4EE' },
    alkaline: { ph: '11.5', use: 'Uso externo · não ingerir', title: 'Água Super Alcalina', description: 'Opção para limpeza pesada e remoção de resíduos em tarefas domésticas.', list: ['Limpeza pesada', 'Remoção de resíduos', 'Não indicada para ingestão'], color: '#E6F4FB' }
  };
  const tabs = document.querySelectorAll('.water-tab');
  const panel = document.getElementById('water-panel');

  tabs.forEach((tab) => tab.addEventListener('click', () => {
    const item = data[tab.dataset.water];
    tabs.forEach((button) => { button.classList.remove('active'); button.setAttribute('aria-selected', 'false'); });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');
    panel.classList.add('changing');
    window.setTimeout(() => {
      document.getElementById('water-ph').textContent = item.ph;
      document.getElementById('water-use').textContent = item.use;
      document.getElementById('water-title').textContent = item.title;
      document.getElementById('water-description').textContent = item.description;
      document.querySelector('.water-meter').style.background = item.color;
      document.getElementById('water-list').innerHTML = item.list.map((entry) => `<li>${entry}</li>`).join('');
      panel.classList.remove('changing');
    }, 180);
  }));
}

function initDemoCarousel() {
  const carousel = document.querySelector('.demo-carousel');
  if (!carousel) return;

  const images = [...carousel.querySelectorAll('.carousel-track img')];
  const previousButton = carousel.querySelector('.carousel-prev');
  const nextButton = carousel.querySelector('.carousel-next');
  let currentIndex = images.findIndex((image) => image.classList.contains('is-active'));

  if (images.length < 2 || !previousButton || !nextButton) return;
  if (currentIndex < 0) currentIndex = 0;

  function showImage(index) {
    currentIndex = (index + images.length) % images.length;
    images.forEach((image, imageIndex) => {
      image.classList.toggle('is-active', imageIndex === currentIndex);
    });
  }

  previousButton.addEventListener('click', () => showImage(currentIndex - 1));
  nextButton.addEventListener('click', () => showImage(currentIndex + 1));
}

function initRevealAnimations() {
  const elements = document.querySelectorAll('.reveal');
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
