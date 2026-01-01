import { useState } from 'react'
import type { ChatMessage } from '@/features/chat/type'

export function useChatSession() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isStreaming, setIsStreaming] = useState(false)

  const sendMessage = async (text: string) => {
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
    }

    setMessages((prev) => [...prev, userMessage])

    setIsStreaming(true)

    const reply = await fetch(`/api/ai/trigger`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'gemini-2.0-flash',
        contents: [{ type: 'text', content: text }],
      }),
    }).then((r) => r.json())

    const placeholder: ChatMessage = {
      id: reply.job_id,
      role: 'assistant',
      content: `等待回覆: job_id=${reply.job_id}`,
    }

    setMessages((prev) => [...prev, placeholder])
    setIsStreaming(false)
  }

  return { messages, sendMessage, isStreaming }
}
