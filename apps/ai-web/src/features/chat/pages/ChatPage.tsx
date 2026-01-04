import { useState } from 'react'
import { ChatMessageList } from '@/ui/organisms/ChatMessageList'
import { ChatInput } from '@/ui/molecules/ChatInput'
import { ModelSelector } from '@/ui/molecules/ModelSelector'
import { ErrorDialog } from '@/ui/molecules/ErrorDialog'
import { ConversationSidebar } from '@/ui/organisms/ConversationSidebar'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Menu } from 'lucide-react'
import { useChatSession } from '../hooks/useChatSession'
import { useModels } from '../hooks/useModels'

export function ChatPage() {
  const [selectedModel, setSelectedModel] = useState('gemini-flash-latest')
  const { messages, sendMessage, isStreaming, error, clearConversation, clearError, conversationId, loadConversation } = useChatSession(selectedModel)
  const { models, loading: modelsLoading } = useModels()
  const [input, setInput] = useState('')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleSubmit = () => {
    if (!input.trim()) return
    sendMessage(input)
    setInput('')
  }

  const handleSelectConversation = async (id: string) => {
    await loadConversation(id)
    setMobileMenuOpen(false) // Close mobile menu after selection
  }

  const handleNewConversation = () => {
    clearConversation()
    setMobileMenuOpen(false)
  }

  return (
    <div className="h-screen flex">
      {/* Desktop Sidebar - Always visible on large screens */}
      <aside className="hidden lg:flex lg:w-64 border-r flex-col">
        <ConversationSidebar
          currentConversationId={conversationId}
          onSelectConversation={handleSelectConversation}
          onNewConversation={handleNewConversation}
        />
      </aside>

      {/* Mobile Sidebar - Sheet overlay with white background */}
      <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
        <SheetContent side="left" className="w-64 p-0 bg-white">
          <ConversationSidebar
            currentConversationId={conversationId}
            onSelectConversation={handleSelectConversation}
            onNewConversation={handleNewConversation}
          />
        </SheetContent>
      </Sheet>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col h-screen">
        {/* Header with consistent height (h-16) to match sidebar */}
        <header className="border-b h-16 px-4 flex items-center justify-between gap-4 flex-shrink-0">
          <div className="flex items-center gap-2">
            {/* Mobile Menu Toggle - Only visible on small screens */}
            <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="lg:hidden">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
            </Sheet>

            <h1 className="font-semibold text-lg">AI Chat</h1>
          </div>

          <div className="flex items-center gap-2">
            {!modelsLoading && models.length > 0 && (
              <ModelSelector
                value={selectedModel}
                onChange={setSelectedModel}
                models={models}
                disabled={isStreaming}
              />
            )}
            <Button
              onClick={handleNewConversation}
              className="bg-[#9fbb44] hover:bg-[#809636] text-white font-medium"
              size="sm"
            >
              New Chat
            </Button>
          </div>
        </header>

        {/* Message Area */}
        <div className="flex-1 overflow-y-auto">
          <ChatMessageList messages={messages} />
        </div>

        {/* Input Area with iOS safe area */}
        <ChatInput
          value={input}
          disabled={isStreaming}
          onChange={setInput}
          onSubmit={handleSubmit}
        />
      </main>

      {/* Error Dialog */}
      <ErrorDialog
        error={error}
        onClose={clearError}
      />
    </div>
  )
}
