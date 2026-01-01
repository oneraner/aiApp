import { cn } from '@/lib/cn'

export function Input(
  props: React.InputHTMLAttributes<HTMLInputElement>
) {
  return (
    <input
      {...props}
      className={cn(
        'w-full rounded-lg border bg-background px-3 py-2 text-sm',
        'focus:outline-none focus:ring-2 focus:ring-primary',
        props.className
      )}
    />
  )
}
