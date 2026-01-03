import { apiClient } from '@/lib/api-client'

export async function triggerAI(params: {
    model: string
    contents: Array<{ type: string; content: string }>
    conversationId?: string
}) {
    return apiClient.triggerAI(params)
}

export function streamResponse(jobId: string) {
    return apiClient.streamResponse(jobId)
}

export async function getConversations() {
    return apiClient.getConversations()
}

export async function getConversation(id: string) {
    return apiClient.getConversation(id)
}

export async function deleteConversation(id: string) {
    return apiClient.deleteConversation(id)
}

export async function getModels() {
    return apiClient.getModels()
}
