import React from 'react'

/**
 * translatedprocesstool
 * inTauritranslated
 */

// translatedIstranslatedinTauritranslated
const isTauri = () => {
  return typeof window !== 'undefined' && Boolean((window as any).__TAURI__ || (window as any).__TAURI_INTERNALS__)
}

/**
 * translated
 * @param url translated'sURL
 */
export const openExternalLink = async (url: string) => {
  try {
    if (isTauri()) {
      // inTauritranslateduseshell API
      const { open } = await import('@tauri-apps/plugin-shell')
      await open(url)
    } else {
      // inWebtranslatedusetranslated
      window.open(url, '_blank', 'noopener,noreferrer')
    }
  } catch (error) {
    console.error('translatedfailed:', error)
    // translatedprocess:translatedusewindow.open
    try {
      window.open(url, '_blank', 'noopener,noreferrer')
    } catch (fallbackError) {
      console.error('translatedfailed:', fallbackError)
      // translated'stranslated:translated
      try {
        await navigator.clipboard.writeText(url)
        alert(`translated:${url}`)
      } catch (clipboardError) {
        console.error('translatedfailed:', clipboardError)
        alert(`translated:${url}`)
      }
    }
  }
}

/**
 * createone canclick'stranslated
 * @param url translated
 * @param text translated
 * @param className CSStranslated
 */
export const ExternalLink: React.FC<{
  url: string
  text: string
  className?: string
}> = ({ url, text, className }) => {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    openExternalLink(url)
  }

  return (
    <a
      href={url}
      onClick={handleClick}
      className={className}
      style={{ 
        color: '#1890ff',
        cursor: 'pointer',
        textDecoration: 'underline'
      }}
    >
      {text}
    </a>
  )
}
