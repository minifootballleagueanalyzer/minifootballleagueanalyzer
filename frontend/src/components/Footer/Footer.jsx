import React, { useState } from 'react';
import { Send, Github, ShieldCheck, X } from 'lucide-react';
import './Footer.css';

const Footer = () => {
  const [status, setStatus] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const modalRef = React.useRef(null);

  // UX/A11Y: Controlar el elemento <dialog> nativo para gestión de foco y teclado
  React.useEffect(() => {
    const modal = modalRef.current;
    if (isModalOpen) {
      modal?.showModal();
    } else {
      modal?.close();
    }
  }, [isModalOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const form = e.target;
    const data = new FormData(form);

    try {
      const response = await fetch('https://formspree.io/f/xwvrzrqv', {
        method: 'POST',
        body: data,
        headers: {
          'Accept': 'application/json'
        }
      });

      if (response.ok) {
        setStatus('SUCCESS');
        form.reset();
        // Cerrar modal automáticamente después de 2 segundos de éxito
        setTimeout(() => {
          setIsModalOpen(false);
          setStatus('');
        }, 2000);
      } else {
        const errorData = await response.json();
        console.error('Error de Formspree:', errorData);
        setStatus('ERROR');
      }
    } catch (error) {
      console.error('Fallo en la petición:', error);
      setStatus('ERROR');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Lógica de renderizado del botón extraída para evitar ternarios anidados (Clean Code)
  const renderButtonContent = () => {
    if (isSubmitting) return <span className="loading-dots">Enviando...</span>;
    if (status === 'SUCCESS') return <>¡Enviado! <ShieldCheck size={18} /></>;
    return <>Enviar Mensaje <Send size={18} /></>;
  };

  return (
    <footer className="main-footer">
      <div className="footer-container">
        <div className="footer-grid">
          <div className="footer-contact-simple">
            <button
              onClick={() => setIsModalOpen(true)}
              className="open-contact-btn"
            >
              <Send size={18} />
              <span>Enviar Mensaje / Feedback</span>
            </button>
          </div>
        </div>

        <div className="footer-bottom">
          <p>© {new Date().getFullYear()} MiniFootball League Analyzer.</p>
          <div className="footer-badges">
            <a href="https://github.com/floatingbit23/minifootballleagueanalyzer" target="_blank" rel="noopener noreferrer" className="footer-github-link" title="Ver código en GitHub">
              <Github size={20} />
            </a>
            <span className="badge">Open Source</span>
            <span className="badge">Real-time Data</span>
          </div>
        </div>
      </div>

      {/* Floating Contact Modal - Native <dialog> handles focus trap and Escape key */}
      <dialog
        ref={modalRef}
        className="contact-modal-native"
        onClose={() => setIsModalOpen(false)}
        onClick={(e) => {
          // Detectar clic en el backdrop (el propio <dialog>) para cerrar
          if (e.target === modalRef.current) setIsModalOpen(false);
        }}
      >
        <div className="contact-modal-content">
          <button
            type="button"
            className="modal-close-btn"
            onClick={() => setIsModalOpen(false)}
            aria-label="Cerrar"
          >
            <X size={20} />
          </button>
          <h4 id="modal-title" className="modal-title">Contacto & Feedback</h4>
          <form onSubmit={handleSubmit} className="contact-form">
            <div className="form-group">
              <input
                type="email"
                name="email"
                placeholder="Tu correo electrónico"
                required
                className="form-input"
              />
            </div>
            <div className="form-group">
              <textarea
                name="message"
                placeholder="¿En qué podemos mejorar?"
                required
                className="form-textarea"
              ></textarea>
            </div>
            <button
              type="submit"
              disabled={isSubmitting}
              className={`submit-btn ${status === 'SUCCESS' ? 'success' : ''}`}
            >
              {renderButtonContent()}
            </button>
            {status === 'ERROR' && (
              <p className="error-msg">Algo salió mal. Por favor, inténtalo de nuevo.</p>
            )}
          </form>
        </div>
      </dialog>
    </footer >
  );
};

export default Footer;
