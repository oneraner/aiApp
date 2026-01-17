'use client'

import { useEffect, useRef } from 'react'
import { ChatBubble } from '@/ui/molecules/ChatBubble'
import { TypingIndicator } from '@/ui/atoms/TypingIndicator'
import { Sparkles, Loader2 } from 'lucide-react'

interface Message {
  id?: string
  role: 'user' | 'assistant'
  content: string
}

interface ChatMessageListProps {
  messages: Message[]
  isStreaming?: boolean
  isLoading?: boolean
}

export function ChatMessageList({ messages, isStreaming = false, isLoading = false }: ChatMessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (!isLoading) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isStreaming, isLoading])

  // Loading State
  if (isLoading) {
    return (
      <div className="space-y-6 px-4 py-8 max-w-3xl mx-auto">
        {[1, 2, 3].map((i) => (
          <div key={i} className={`flex flex-col ${i % 2 === 0 ? 'items-end' : 'items-start'} space-y-2 opacity-50`}>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 rounded-full bg-muted animate-pulse" />
              <div className="h-4 w-20 bg-muted rounded animate-pulse" />
            </div>
            <div className={`h-16 w-full max-w-md bg-muted rounded-2xl animate-pulse ${i % 2 === 0 ? 'rounded-tr-none' : 'rounded-tl-none'}`} />
          </div>
        ))}
        <div className="flex justify-center pt-4">
          <Loader2 className="h-6 w-6 animate-spin text-primary/50" />
        </div>
      </div>
    )
  }

  // Empty State
  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center space-y-6 max-w-md px-4">
          <div className="w-20 h-20 mx-auto rounded-3xl bg-gradient-to-br from-primary/30 via-primary/20 to-accent flex items-center justify-center shadow-lg shadow-primary/10">
            <Sparkles className="w-10 h-10 text-primary" />
          </div>
          <div className="space-y-2">
            <h2 className="text-2xl font-semibold text-foreground">開始對話</h2>
            <p className="text-muted-foreground">
              詢問任何關於程式設計、知識問答或創意任務的問題
            </p>
          </div>
          {/* Quick suggestions */}
          <div className="flex flex-wrap justify-center gap-2 pt-2">
            {['解釋程式碼', '寫一篇文章', '解答問題'].map((text) => (
              <span
                key={text}
                className="px-3 py-1.5 text-sm bg-secondary text-secondary-foreground rounded-full border border-border"
              >
                {text}
              </span>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // Messages List
  return (
    <div className="space-y-4 px-4 py-6 max-w-3xl mx-auto">
      {messages.map((m, i) => (
        <div key={m.id || i} className="animate-in fade-in slide-in-from-bottom-2">
          <ChatBubble role={m.role} content={m.content} />
        </div>
      ))}

      {/* Show typing indicator when streaming and last message is from user or assistant content is empty */}
      {isStreaming && messages.length > 0 && (messages[messages.length - 1].content === '' || messages[messages.length - 1].role === 'user') && (
        <TypingIndicator />
      )}

      {/* Scroll anchor */}
      <div ref={bottomRef} />
    </div>
  )
}
