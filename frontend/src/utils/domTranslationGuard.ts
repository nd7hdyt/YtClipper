/**
 * translated「translated」（Chrome / Edge / Safari）translated translated <font> Packagetranslated'stranslated。
 * React translatedthistranslated removeChild / insertBefore translated，translatedintranslated'stranslated，
 * translated NotFoundError，translated ErrorBoundary translated（issue #100：Docker Web translated
 * translatedusertranslated LLM Providesprovidertranslated）。
 *
 * thistranslated thistranslated  DOM translated「translated → skip / translated」，
 * translatedIstranslatedcantranslated，translated。translated facebook/react#11538 'stranslated。
 */

const GUARD_FLAG = '__autoclipDomTranslationGuard'

export function isPageTranslated(): boolean {
  if (typeof document === 'undefined') return false
  const html = document.documentElement
  return (
    html.classList.contains('translated-ltr') ||
    html.classList.contains('translated-rtl') ||
    // Safari / translated Chrome versiontranslated class，translated's <font> translated
    !!document.querySelector('font[style*="vertical-align: inherit"] > font')
  )
}

export function isDomDisplacementError(error: unknown): boolean {
  const message = error instanceof Error ? error.message : String(error ?? '')
  return (
    /removeChild|insertBefore/.test(message) &&
    /not a child of this node|NotFoundError/i.test(message)
  )
}

export function installDomTranslationGuard(): void {
  if (typeof Node === 'undefined') return
  const proto = Node.prototype as Node & Record<string, unknown>
  if (proto[GUARD_FLAG]) return
  proto[GUARD_FLAG] = true

  const originalRemoveChild = Node.prototype.removeChild
  Node.prototype.removeChild = function removeChild<T extends Node>(this: Node, child: T): T {
    if (child.parentNode !== this) {
      if (import.meta.env.DEV) {
        console.warn('[dom-guard] removeChild skip：translatedetc.translated', child)
      }
      return child
    }
    return originalRemoveChild.call(this, child) as T
  }

  const originalInsertBefore = Node.prototype.insertBefore
  Node.prototype.insertBefore = function insertBefore<T extends Node>(
    this: Node,
    newNode: T,
    referenceNode: Node | null,
  ): T {
    if (referenceNode && referenceNode.parentNode !== this) {
      if (import.meta.env.DEV) {
        console.warn('[dom-guard] insertBefore Referencetranslated，translated', referenceNode)
      }
      return originalInsertBefore.call(this, newNode, null) as T
    }
    return originalInsertBefore.call(this, newNode, referenceNode) as T
  }
}
