// Message types
export interface ChatMessage {
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp?: Date
    model?: string
}

// API response types
export interface TriggerAIResponse {
    job_id: string
    conversation_id: string
}

export interface Conversation {
    id: string
    created_at: string
    updated_at: string
    message_count: number
}

export interface ConversationDetail extends Conversation {
    messages: ConversationMessage[]
}

export interface ConversationMessage {
    id: string
    role: string
    content: string
    model_used: string | null
    created_at: string
}

export interface Model {
    name: string
    provider: string
    capabilities: string[]
}

// API Error types
export interface APIError {
    detail?: string | { error?: string; message?: string }
    status?: number
}

// Rate limit types
export interface RateLimitStatus {
    used?: number
    remaining?: number
    limit?: number
    reset_time?: string
}
