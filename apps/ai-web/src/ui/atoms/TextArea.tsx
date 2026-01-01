import { cn } from '@/lib/cn'

export function TextArea(
  props: React.TextareaHTMLAttributes<HTMLTextAreaElement>
) {
  return (
    <textarea
      {...props}
      className={cn(
        'w-full resize-none rounded-xl border bg-background px-3 py-2 text-sm',
        'focus:outline-none focus:ring-2 focus:ring-primary',
        props.className
      )}
    />
  )
}
