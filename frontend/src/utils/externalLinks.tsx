import React from 'react'

/**
 * EN
 * ENTauriin environmentENOpen external link
 */

// ENTauriin environment
const isTauri = () => {
  return typeof window !== 'undefined' && Boolean((window as any).__TAURI__ || (window as any).__TAURI_INTERNALS__)
}

/**
 * Open external link
 * @param url ENURL
 */
export const openExternalLink = async (url: string) => {
  try {
    if (isTauri()) {
      // ENTauriin environmentENshell API
      const { open } = await import('@tauri-apps/plugin-shell')
      await open(url)
    } else {
      // ENWebin environmentENNormalEN
      window.open(url, '_blank', 'noopener,noreferrer')
    }
  } catch (error) {
    console.error('Open external linkFailed:', error)
    // EN:ENwindow.open
    try {
      window.open(url, '_blank', 'noopener,noreferrer')
    } catch (fallbackError) {
      console.error('ENFailed:', fallbackError)
      // EN:ENtoEN
      try {
        await navigator.clipboard.writeText(url)
        alert(`ENtoEN:${url}`)
      } catch (clipboardError) {
        console.error('ENtoENFailed:', clipboardError)
        alert(`EN:${url}`)
      }
    }
  }
}

/**
 * EN
 * @param url EN
 * @param text ENText
 * @param className CSSEN
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
