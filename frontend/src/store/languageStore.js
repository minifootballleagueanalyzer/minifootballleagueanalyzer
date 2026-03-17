import { atom } from 'nanostores';

// Idioma por defecto: español
export const languageStore = atom('es');

export function toggleLanguage() {
  const current = languageStore.get();
  languageStore.set(current === 'es' ? 'en' : 'es');
}
