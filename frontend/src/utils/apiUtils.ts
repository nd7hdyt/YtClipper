/**
 * APIEN
 * ENAPI URLENrequest
 */

import { apiConfigManager, getApiBaseUrl, buildApiUrl } from './apiConfig'

// ENfetchAPIENURL
export const getApiBaseUrlAsync = async () => {
  // waiting API configEN
  await apiConfigManager.waitForReady(5000);
  return getApiBaseUrl();
}

// ENAPI URL
export const buildApiUrlAsync = async (path: string) => {
  // waiting API configEN
  await apiConfigManager.waitForReady(5000);
  return buildApiUrl(path);
}

// unifiedfetchEN
export const apiFetch = async (path: string, options?: RequestInit) => {
  const url = await buildApiUrlAsync(path);
  return fetch(url, options);
}

// unifiedGETrequest
export const apiGet = async (path: string) => {
  return apiFetch(path, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

// unifiedPOSTrequest
export const apiPost = async (path: string, data?: any) => {
  return apiFetch(path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: data ? JSON.stringify(data) : undefined,
  })
}

// unifiedPUTrequest
export const apiPut = async (path: string, data?: any) => {
  return apiFetch(path, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: data ? JSON.stringify(data) : undefined,
  })
}

// unifiedDELETErequest
export const apiDelete = async (path: string) => {
  return apiFetch(path, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  })
}
