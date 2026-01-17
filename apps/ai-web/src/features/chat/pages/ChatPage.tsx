'use client'

import { useState } from 'react'
import { ChatMessageList } from '@/ui/organisms/ChatMessageList'
import { ChatInput } from '@/ui/molecules/ChatInput'
import { ModelSelector } from '@/ui/molecules/ModelSelector'
import { ErrorDialog } from '@/ui/molecules/ErrorDialog'
import { ConversationSidebar } from '@/ui/organisms/ConversationSidebar'
import { ThemeToggle } from '@/ui/atoms/ThemeToggle'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Menu, Plus, Sparkles } from 'lucide-react'
import { useChatSession } from '../hooks/useChatSession'
import { useModels } from '../hooks/useModels'

export function ChatPage() {
  const [selectedModel, setSelectedModel] = useState('gemini-flash-latest')
  const { messages, sendMessage, isStreaming, isLoadingMessages, error, clearConversation, clearError, conversationId, loadConversation } = useChatSession(selectedModel)
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
    setMobileMenuOpen(false)
  }

  const handleNewConversation = () => {
    clearConversation()
    setMobileMenuOpen(false)
  }

  return (
    <div className="h-screen flex bg-background">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:w-64 border-r border-border flex-col bg-card" role="complementary">
        <ConversationSidebar
          currentConversationId={conversationId}
          onSelectConversation={handleSelectConversation}
          onNewConversation={handleNewConversation}
        />
      </aside>

      {/* Mobile Sidebar */}
      <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
        <SheetContent side="left" className="w-64 p-0 bg-card border-border">
          <ConversationSidebar
            currentConversationId={conversationId}
            onSelectConversation={handleSelectConversation}
            onNewConversation={handleNewConversation}
          />
        </SheetContent>
      </Sheet>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col h-screen bg-background" role="main">
        {/* Header */}
        <header className="border-b border-border h-16 px-3 sm:px-4 flex items-center justify-between gap-2 sm:gap-4 flex-shrink-0 bg-card">
          <div className="flex items-center gap-3">
            {/* Mobile Menu Toggle */}
            <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="lg:hidden" aria-label="開啟選單">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
            </Sheet>

            {/* Logo/Title with gradient */}
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-purple-500 flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <h1 className="font-bold text-lg hidden sm:block gradient-text">AI Chat</h1>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            <ThemeToggle />

            {!modelsLoading && models.length > 0 && (
              <ModelSelector
                value={selectedModel}
                onChange={setSelectedModel}
                models={models}
                disabled={isStreaming}
              />
            )}

            {/* New Chat Button with glow effect */}
            <Button
              onClick={handleNewConversation}
              className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold btn-glow"
              size="sm"
              aria-label="開始新對話"
            >
              <Plus className="h-4 w-4" />
              <span className="hidden sm:inline ml-1">新對話</span>
            </Button>
          </div>
        </header>

        {/* Message Area */}
        <div className="flex-1 overflow-y-auto">
          <ChatMessageList messages={messages} isStreaming={isStreaming} isLoading={isLoadingMessages} />
        </div>

        {/* Input Area */}
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
