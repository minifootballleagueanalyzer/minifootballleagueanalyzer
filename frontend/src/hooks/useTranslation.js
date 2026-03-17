import { useStore } from '@nanostores/react';
import { languageStore } from '../store/languageStore';
import { ui } from '../i18n/traducciones';

export function useTranslation() {
  const language = useStore(languageStore);

  const t = (key) => {
    return ui[language][key] || key;
  };

  return { t, language };
}
