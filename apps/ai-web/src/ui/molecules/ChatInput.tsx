import { TextArea } from '@/ui/atoms/TextArea'
import { Button } from '@/components/ui/button'
import { Send } from 'lucide-react'

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
  return (
    <div className="border-t p-4 bg-background">
      <div className="max-w-3xl mx-auto flex gap-2">
        <TextArea
          rows={2}
          value={value}
          disabled={disabled}
          placeholder="Type your message..."
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              onSubmit()
            }
          }}
        />
        <Button
          disabled={disabled || !value.trim()}
          onClick={onSubmit}
          className="h-auto bg-[#9fbb44] hover:bg-[#809636] text-white font-medium"
        >
          <Send className="h-4 w-4 mr-2" />
          Send
        </Button>
      </div>
    </div>
  )
}
