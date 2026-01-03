import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api-client'

interface Conversation {
    id: string
    created_at: string
    updated_at: string
    message_count: number
}

export function useConversations() {
    const [conversations, setConversations] = useState<Conversation[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const fetchConversations = async () => {
        setLoading(true)
        setError(null)
        try {
            const data = await apiClient.getConversations()
            setConversations(data)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load conversations')
        } finally {
            setLoading(false)
        }
    }

    const deleteConversation = async (id: string) => {
        try {
            await apiClient.deleteConversation(id)
            // Remove from local state
            setConversations(prev => prev.filter(c => c.id !== id))
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to delete conversation')
            throw err
        }
    }

    // Auto-fetch on mount
    useEffect(() => {
        fetchConversations()
    }, [])

    return {
        conversations,
        loading,
        error,
        fetchConversations,
        deleteConversation,
    }
}
