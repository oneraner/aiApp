import { TextArea } from '@/ui/atoms/TextArea'
import { Button } from '@/ui/atoms/Button'

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
    <div className="border-t p-4">
      <div className="max-w-3xl mx-auto flex gap-2">
        <TextArea
          rows={2}
          value={value}
          disabled={disabled}
          placeholder="Message..."
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              onSubmit()
            }
          }}
        />
        <Button disabled={disabled} onClick={onSubmit}>
          Send
        </Button>
      </div>
    </div>
  )
}
