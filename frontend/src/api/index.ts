import { liveApi } from './client'
import { mockApi } from './mock'
import type { Api } from './types'

/** VITE_MOCK=1 swaps every endpoint and the SSE stream for the in-browser mock. */
export const api: Api = import.meta.env.VITE_MOCK === '1' ? mockApi : liveApi

export * from './types'
