import { ChatBubble } from '@/ui/molecules/ChatBubble'

export function ChatMessageList({
  messages,
}: {
  messages: { role: 'user' | 'assistant'; content: string }[]
}) {
  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-muted-foreground">
        <div className="text-center space-y-2">
          <p className="text-lg">Ask anything</p>
          <p className="text-sm">AI assistant</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4 px-4 py-6 max-w-3xl mx-auto">
      {messages.map((m, i) => (
        <ChatBubble key={i} role={m.role} content={m.content} />
      ))}
    </div>
  )
}
