export function ChatBubble({
  role,
  content,
}: {
  role: 'user' | 'assistant'
  content: string
}) {
  const isUser = role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`
          max-w-[80%] rounded-2xl px-4 py-2 text-sm whitespace-pre-wrap
          ${isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-foreground'}
        `}
      >
        {content}
      </div>
    </div>
  )
}
