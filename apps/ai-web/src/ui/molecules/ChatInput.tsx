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

  return (
    <div className="border-t p-4 bg-background">
      <div className="max-w-3xl mx-auto space-y-2">
        <TextArea
          rows={2}
          value={value}
          disabled={disabled}
          placeholder={`輸入訊息...（限制 ${MAX_CHARS} 字元）`}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              if (!disabled && value.trim() && !isOverLimit) {
                onSubmit()
              }
            }
          }}
        />

        <div className="flex items-center justify-between">
          {/* Character counter */}
          <div className={`text-xs ${isOverLimit ? 'text-red-500 font-medium' : 'text-gray-500'}`}>
            {charCount} / {MAX_CHARS} 字元
            {isOverLimit && ' - 超過限制！'}
          </div>

          <Button
            disabled={disabled || !value.trim() || isOverLimit}
            onClick={onSubmit}
            className="h-auto bg-[#9fbb44] hover:bg-[#809636] text-white font-medium"
          >
            <Send className="h-4 w-4 mr-2" />
            Send
          </Button>
        </div>
      </div>
    </div>
  )
}
