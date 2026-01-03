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
          max-w-[80%] rounded-2xl px-4 py-3 text-sm whitespace-pre-wrap
          ${isUser
            ? 'bg-[#9fbb44] text-white font-medium'
            : 'bg-[#f7f2ee] text-gray-800 border border-[#dfc9b9]'}
        `}
      >
        {content}
      </div>
    </div>
  )
}
