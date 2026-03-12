import { useState, useRef, useEffect } from 'react';
import './ChatbotWidget.css';

// Preguntas predefinidas que el usuario puede hacer
const PRESET_QUESTIONS = [
  '¿Quién lidera la 1ª División?',
  '¿Cuál es el mejor equipo de la 2ª División Grupo A?',
  '¿Cuál es el mejor equipo de la 2ª División Grupo B?',
  '¿Quién lidera la 3ª División Grupo A?',
  '¿Quién lidera la 3ª División Grupo B?',
  '¿Quién lidera la 4ª División?',
  '¿Cuál es el ranking ELO completo de la 1ª División?',
  '¿Qué equipo tiene más puntos ELO en toda la liga?',
];

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: '¡Hola! Soy el analista de la MiniFootball League 🟢 Selecciona una pregunta para empezar.',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  async function askQuestion(question) {
    if (loading) return;

    setMessages((prev) => [...prev, { role: 'user', text: question }]);
    setLoading(true);

    try {
      const res = await fetch('/api/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: data.answer || data.error || 'Sin respuesta.' },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Error de conexión. Inténtalo de nuevo.' },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setMessages([
      {
        role: 'assistant',
        text: '¡Hola! Soy el analista de la MiniFootball League 🟢 Selecciona una pregunta para empezar.',
      },
    ]);
  }

  return (
    <>
      {/* Ventana del chat */}
      <div className={`chatbot-window ${isOpen ? 'chatbot-window--open' : ''}`}>
        {/* Header del chat */}
        <div className="chatbot-header">
          <div className="chatbot-header__info">
            <div className="chatbot-header__avatar">
              <span>⚽</span>
            </div>
            <div>
              <p className="chatbot-header__title">Analista MFL</p>
              <p className="chatbot-header__subtitle">Powered by Gemini</p>
            </div>
          </div>
          <div className="chatbot-header__actions">
            <button
              className="chatbot-header__btn"
              onClick={handleReset}
              title="Reiniciar chat"
              aria-label="Reiniciar chat"
            >
              ↺
            </button>
            <button
              className="chatbot-header__btn"
              onClick={() => setIsOpen(false)}
              title="Cerrar"
              aria-label="Cerrar chatbot"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Mensajes */}
        <div className="chatbot-messages">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`chatbot-bubble chatbot-bubble--${msg.role}`}
            >
              {msg.text}
            </div>
          ))}
          {loading && (
            <div className="chatbot-bubble chatbot-bubble--assistant chatbot-bubble--loading">
              <span /><span /><span />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Preguntas predefinidas */}
        <div className="chatbot-presets">
          <p className="chatbot-presets__label">Preguntas rápidas</p>
          <div className="chatbot-presets__grid">
            {PRESET_QUESTIONS.map((q) => (
              <button
                key={q}
                className="chatbot-preset-btn"
                onClick={() => askQuestion(q)}
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Botón flotante */}
      <button
        className={`chatbot-fab ${isOpen ? 'chatbot-fab--open' : ''}`}
        onClick={() => setIsOpen((v) => !v)}
        aria-label={isOpen ? 'Cerrar chatbot' : 'Abrir chatbot'}
      >
        <span className="chatbot-fab__icon chatbot-fab__icon--chat">⚽</span>
        <span className="chatbot-fab__icon chatbot-fab__icon--close">✕</span>
      </button>
    </>
  );
}
