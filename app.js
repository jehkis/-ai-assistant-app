document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");
  const chatStatus = document.querySelector(".chat-status");
  const demoReplies = [
    "Hei! Tämä on AI Assistant -prototyyppi, joka osoittaa modernin dark UI:n ja responsive designin.",
    "Sivuston tavoitteena on näyttää hyvää käytettävyyttä ja visuaalista ilmettä ennen varsinaisen tekoäly-taustapalvelun rakentamista.",
    "Sivulla on About-sivu jossa kerrotaan lisää, Projects-sivu esimerkkiprojekteista, ja Contact-sivu yhteydenottoa varten.",
    "Vieraile About-sivulla saadaksesi lisää tietoa tämän prototypin tarkoituksesta ja rakenteesta!",
  ];
  let demoIndex = 0;

  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
  }

  const chatForm = document.querySelector(".chat-input");
  const chatList = document.querySelector(".chat-history");
  const prompt = document.getElementById("prompt");
  const sendButton = chatForm?.querySelector('button[type="submit"]') || null;
  const resetButton = document.querySelector("[data-reset-chat]");

  if (chatForm && chatList && prompt) {
    chatForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const value = prompt.value.trim();
      if (!value) return;

      chatList.appendChild(createMessage("You", value, "user"));
      prompt.value = "";
      chatList.scrollTop = chatList.scrollHeight;

      const loadingMessage = createMessage("Assistant", "Täytetään seuraava kohta...", "bot is-loading");
      chatList.appendChild(loadingMessage);
      setChatStatus("Täytetään kohtia järjestyksessä...", "loading");

      if (sendButton) {
        sendButton.disabled = true;
        sendButton.textContent = "Täytetään...";
      }

      try {
        const reply = await getDemoReply(value);
        loadingMessage.replaceWith(createMessage("Assistant", reply, "bot"));
        setChatStatus("Kohta täytetty.", "idle");
      } catch (error) {
        console.error(error);
        loadingMessage.replaceWith(
          createMessage("Assistant", "Tässä demossa täyttö epäonnistui, yritä uudelleen.", "bot")
        );
        setChatStatus("Demo ei saanut seuraavaa kohtaa valmiiksi.", "error");
      } finally {
        chatList.scrollTop = chatList.scrollHeight;
        if (sendButton) {
          sendButton.disabled = false;
          sendButton.textContent = "Send";
        }
      }
    });
  }

  if (resetButton && chatList) {
    resetButton.addEventListener("click", () => {
      demoIndex = 0;
      chatList.replaceChildren();
      setChatStatus("Valmis aloittamaan.", "idle");
    });
  }

  const contactForm = document.querySelector(".contact-form");
  const status = document.querySelector(".form-status");

  if (contactForm && status) {
    contactForm.addEventListener("submit", (event) => {
      event.preventDefault();
      status.textContent = "Viestiä ei lähetetä tässä prototyypissä. Lomake toimii vain käyttöliittymänä.";
    });
  }

  async function getDemoReply(message) {
    await new Promise((resolve) => window.setTimeout(resolve, 450));
    const reply = demoReplies[demoIndex] || `Seuraava täytettävä kohta on: ${message}`;
    demoIndex += 1;
    return reply;
  }

  function setChatStatus(text, state) {
    if (!chatStatus) return;
    chatStatus.textContent = text;
    chatStatus.classList.toggle("is-loading", state === "loading");
    chatStatus.classList.toggle("is-error", state === "error");
  }

  function createMessage(author, text, className) {
    const item = document.createElement("li");
    item.className = `msg ${className}`;

    const label = document.createElement("strong");
    label.textContent = `${author}:`;

    item.append(label, document.createTextNode(` ${text}`));
    return item;
  }
});