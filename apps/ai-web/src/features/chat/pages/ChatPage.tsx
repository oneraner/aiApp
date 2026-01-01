import { useState } from 'react'
import { ChatMessageList } from '@/ui/organisms/ChatMessageList'
import { ChatInput } from '@/ui/molecules/ChatInput'
import { useChatSession } from '../hooks/useChatSession'

export function ChatPage() {
  const { messages, sendMessage, isStreaming } = useChatSession()
  const [input, setInput] = useState('')

  return (
    <div className="h-screen flex flex-col">
      <header className="h-14 border-b flex items-center px-4">
        AI Chat
      </header>

      <main className="flex-1 overflow-y-auto">
        <ChatMessageList messages={messages} />
      </main>

      <ChatInput
        value={input}
        disabled={isStreaming}
        onChange={setInput}
        onSubmit={() => {
          sendMessage(input)
          setInput('')
        }}
      />
    </div>
  )
}
