'use client'

import { TextArea } from '@/ui/atoms/TextArea'
import { Button } from '@/components/ui/button'
import { Send } from 'lucide-react'

const MAX_CHARS = 300

export function ChatInput({
  value,
  disabled,
  onChange,
  onSubmit,
}: {
  value: string
  disabled?: boolean
  onChange: (v: string) => void
  onSubmit: () => void
}) {
  const charCount = value.length
  const isOverLimit = charCount > MAX_CHARS
  const canSubmit = !disabled && value.trim() && !isOverLimit

  return (
    <div className="border-t border-border p-3 sm:p-4 bg-card w-full" style={{ paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom))' }}>
      <div className="max-w-3xl mx-auto space-y-3 w-full">
        <TextArea
          rows={2}
          value={value}
          disabled={disabled}
          placeholder={`輸入訊息...（Ctrl+Enter 發送，限制 ${MAX_CHARS} 字元）`}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            // Ctrl+Enter (Windows/Linux) or Cmd+Enter (Mac) to send
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey) && canSubmit) {
              e.preventDefault()
              onSubmit()
            }
          }}
          className="bg-background border-border text-foreground placeholder:text-muted-foreground"
        />

        <div className="flex items-center justify-between">
          {/* Character counter */}
          <div className={`text-xs ${isOverLimit ? 'text-destructive font-medium' : 'text-muted-foreground'}`}>
            {charCount} / {MAX_CHARS} 字元
            {isOverLimit && ' - 超過限制！'}
          </div>

          <Button
            disabled={!canSubmit}
            onClick={onSubmit}
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold shadow-lg hover:shadow-xl transition-all duration-200 btn-glow"
            aria-label="發送訊息"
          >
            <Send className="h-4 w-4 mr-2" />
            發送
          </Button>
        </div>
      </div>
    </div>
  )
}
