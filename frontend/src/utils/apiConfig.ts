/**
 * API configEN
 * ENportconfig
 */

interface ApiConfig {
  baseUrl: string;
  port: number;
  isReady: boolean;
}

class ApiConfigManager {
  private static instance: ApiConfigManager;
  private config: ApiConfig = {
    baseUrl: '/api/v1',
    port: 0,
    isReady: false
  };
  private listeners: Array<(config: ApiConfig) => void> = [];

  private constructor() {
    this.initializeConfig();
  }

  static getInstance(): ApiConfigManager {
    if (!ApiConfigManager.instance) {
      ApiConfigManager.instance = new ApiConfigManager();
    }
    return ApiConfigManager.instance;
  }

  private async initializeConfig() {
    // checkEN Tauri in environment
    if (typeof window !== 'undefined' && ((window as any).__TAURI__ || (window as any).__TAURI_INTERNALS__)) {
      try {
        // EN
        const { listen } = await import('@tauri-apps/api/event');
        const { invoke } = await import('@tauri-apps/api/core');
        
        await listen('backend-started', (event: any) => {
          const backendStatus = event.payload;
          if (backendStatus && backendStatus.port) {
            this.updateFromPort(backendStatus.port);
          }
        });

        const backendStatus = await invoke('get_service_status') as any;
        if (backendStatus?.is_running && backendStatus?.port) {
          this.updateFromPort(backendStatus.port);
        }

        // ENfetchconfig
        if ((window as any).__BACKEND_BASE__) {
          this.updateConfig({
            baseUrl: (window as any).__BACKEND_BASE__,
            port: this.extractPortFromUrl((window as any).__BACKEND_BASE__),
            isReady: true
          });
        }
      } catch (error) {
        console.warn('EN Tauri EN:', error);
      }
    }
  }

  private updateFromPort(port: number) {
    this.updateConfig({
      baseUrl: `http://127.0.0.1:${port}/api/v1`,
      port,
      isReady: true
    });
  }

  private extractPortFromUrl(url: string): number {
    const match = url.match(/:(\d+)/);
    return match ? parseInt(match[1], 10) : 0;
  }

  private updateConfig(newConfig: Partial<ApiConfig>) {
    this.config = { ...this.config, ...newConfig };
    this.notifyListeners();
  }

  private notifyListeners() {
    // waitForReady ENremove；EN forEach EN，
    // EN 2、4… ENrequestEN 30s EN（settingsEN）
    [...this.listeners].forEach(listener => listener(this.config));
  }

  /**
   * fetchEN API config
   */
  getConfig(): ApiConfig {
    return { ...this.config };
  }

  /**
   * fetch API EN URL
   */
  getBaseUrl(): string {
    return this.config.baseUrl;
  }

  /**
   * check API EN
   */
  isReady(): boolean {
    return this.config.isReady;
  }

  /**
   * addconfigChangeEN
   */
  addListener(listener: (config: ApiConfig) => void): () => void {
    this.listeners.push(listener);
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  /**
   * waiting API EN
   */
  async waitForReady(timeout: number = 30000): Promise<boolean> {
    if (this.isReady()) {
      return true;
    }

    return new Promise((resolve) => {
      const timeoutId = setTimeout(() => {
        resolve(false);
      }, timeout);

      const removeListener = this.addListener((config) => {
        if (config.isReady) {
          clearTimeout(timeoutId);
          removeListener();
          resolve(true);
        }
      });
    });
  }

  /**
   * EN API URL
   */
  buildUrl(path: string): string {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;
    return `${this.config.baseUrl}${normalizedPath}`;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(this.buildUrl('/health'), {
        method: 'GET',
        timeout: 5000
      } as any);
      return response.ok;
    } catch (error) {
      console.warn('API Health checkFailed:', error);
      return false;
    }
  }
}

// EN
export const apiConfigManager = ApiConfigManager.getInstance();

// EN
export const getApiBaseUrl = () => apiConfigManager.getBaseUrl();
export const isApiReady = () => apiConfigManager.isReady();
export const waitForApiReady = (timeout?: number) => apiConfigManager.waitForReady(timeout);
export const buildApiUrl = (path: string) => apiConfigManager.buildUrl(path);
export const checkApiHealth = () => apiConfigManager.healthCheck();
