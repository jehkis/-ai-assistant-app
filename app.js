document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");

  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
  }

  const temp = document.getElementById("temp");
  const tempOut = document.getElementById("tempOut");

  if (temp && tempOut) {
    const syncTemperature = () => {
      tempOut.value = temp.value;
    };

    temp.addEventListener("input", syncTemperature);
    syncTemperature();
  }

  const chatForm = document.querySelector(".chat-input");
  const chatList = document.querySelector(".chat-history");
  const prompt = document.getElementById("prompt");

  if (chatForm && chatList && prompt) {
    chatForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const value = prompt.value.trim();
      if (!value) return;

      chatList.appendChild(createMessage("You", value, "user"));
      prompt.value = "";
      chatList.scrollTop = chatList.scrollHeight;

      window.setTimeout(() => {
        chatList.appendChild(createMessage("Assistant", "Tämä on mock-vastaus.", "bot"));
        chatList.scrollTop = chatList.scrollHeight;
      }, 700);
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

  function createMessage(author, text, className) {
    const item = document.createElement("li");
    item.className = `msg ${className}`;

    const label = document.createElement("strong");
    label.textContent = `${author}:`;

    item.append(label, document.createTextNode(` ${text}`));
    return item;
  }
});