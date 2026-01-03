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
      <div className="flex-1 flex flex-col">
        <header className="h-14 border-b flex items-center justify-between px-4 bg-background">
          <div className="flex items-center gap-3">
            {/* Mobile Menu Button */}
            <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="lg:hidden">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
            </Sheet>

            <h1 className="font-semibold text-lg">AI Chat</h1>

            {!modelsLoading && models.length > 0 && (
              <div className="hidden sm:block">
                <ModelSelector
                  value={selectedModel}
                  onChange={setSelectedModel}
                  models={models}
                  disabled={isStreaming}
                />
              </div>
            )}
          </div>

          {/* New Chat button - Always visible with solid styling */}
          <Button
            onClick={handleNewConversation}
            className="bg-[#9fbb44] hover:bg-[#809636] text-white font-medium"
            size="sm"
          >
            New Chat
          </Button>
        </header>

        <main className="flex-1 overflow-y-auto">
          <ChatMessageList messages={messages} />
        </main>

        <ChatInput
          value={input}
          disabled={isStreaming}
          onChange={setInput}
          onSubmit={handleSubmit}
        />

        <ErrorDialog
          error={error}
          onClose={clearError}
        />
      </div>
    </div>
  )
}
