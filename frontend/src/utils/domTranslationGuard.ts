/**
 * EN「EN」（Chrome / Edge / Safari）ENTextEN <font> EN。
 * React EN removeChild / insertBefore EN，EN，
 * EN NotFoundError，EN ErrorBoundary uninstall（issue #100：Docker Web EN
 * EN LLM EN）。
 *
 * EN DOM ActionsEN「EN → EN / ENtoEN」，
 * EN，EN。EN facebook/react#11538 EN。
 */

const GUARD_FLAG = '__autoclipDomTranslationGuard'

export function isPageTranslated(): boolean {
  if (typeof document === 'undefined') return false
  const html = document.documentElement
  return (
    html.classList.contains('translated-ltr') ||
    html.classList.contains('translated-rtl') ||
    // Safari / EN Chrome versionEN class，EN <font> EN
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
        console.warn('[dom-guard] removeChild EN：EN', child)
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
        console.warn('[dom-guard] insertBefore EN，ENtoEN', referenceNode)
      }
      return originalInsertBefore.call(this, newNode, null) as T
    }
    return originalInsertBefore.call(this, newNode, referenceNode) as T
  }
}
