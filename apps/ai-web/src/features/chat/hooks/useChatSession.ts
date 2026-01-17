import { useState, useRef } from 'react'
import type { ChatMessage } from '@/features/chat/type'
import { apiClient } from '@/lib/api-client'

export function useChatSession(selectedModel: string = 'gemini-flash-latest') {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [isLoadingMessages, setIsLoadingMessages] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const conversationIdRef = useRef<string | null>(null)

  const sendMessage = async (text: string) => {
    setError(null)

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
    }

    setMessages((prev) => [...prev, userMessage])
    setIsStreaming(true)

    try {
      // Trigger AI with backend
      const result = await apiClient.triggerAI({
        model: selectedModel,
        contents: [{ type: 'text', content: text }],
        conversationId: conversationIdRef.current || undefined,
      })

      // Save conversation ID for future messages
      conversationIdRef.current = result.conversation_id

      // Create placeholder for assistant message
      const assistantMessageId = result.job_id
      const assistantMessage: ChatMessage = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
      }

      setMessages((prev) => [...prev, assistantMessage])

      // Connect to SSE stream
      const eventSource = apiClient.streamResponse(result.job_id)

      eventSource.onmessage = (event) => {
        const chunk = event.data

        if (chunk === '[DONE]') {
          eventSource.close()
          setIsStreaming(false)
          return
        }

        // Check if chunk is an error message
        if (chunk.startsWith('❌')) {
          eventSource.close()
          setIsStreaming(false)
          // Extract error message (remove ❌ prefix)
          const errorMsg = chunk.replace('❌ ', '')
          setError(errorMsg)

          // Update assistant message to show error
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessageId
                ? { ...msg, content: `發生錯誤：${errorMsg}` }
                : msg
            )
          )
          return
        }

        // Append chunk to assistant message
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessageId
              ? { ...msg, content: msg.content + chunk }
              : msg
          )
        )
      }

      eventSource.onerror = (err) => {
        console.error('SSE error:', err)
        eventSource.close()
        setIsStreaming(false)
        setError('串流連接錯誤')
      }
    } catch (err) {
      setIsStreaming(false)
      const errorMsg = err instanceof Error ? err.message : '發送訊息失敗'
      setError(errorMsg)

      // Show error in chat
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `錯誤：${errorMsg}`,
        },
      ])
    }
  }

  const loadConversation = async (conversationId: string) => {
    setIsLoadingMessages(true)
    setError(null)
    try {
      const conversation = await apiClient.getConversation(conversationId)
      conversationIdRef.current = conversation.id

      setMessages(
        conversation.messages.map((msg) => ({
          id: msg.id,
          role: msg.role as 'user' | 'assistant',
          content: msg.content,
        }))
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : '載入對話失敗')
    } finally {
      setIsLoadingMessages(false)
    }
  }

  const clearConversation = () => {
    conversationIdRef.current = null
    setMessages([])
    setError(null)
  }

  const clearError = () => {
    setError(null)
  }

  return {
    messages,
    sendMessage,
    isStreaming,
    isLoadingMessages,
    error,
    loadConversation,
    clearConversation,
    clearError,
    conversationId: conversationIdRef.current
  }
}
