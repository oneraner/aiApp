import { cn } from '@/lib/cn'

export function IconButton(
  props: React.ButtonHTMLAttributes<HTMLButtonElement>
) {
  return (
    <button
      {...props}
      className={cn(
        'inline-flex items-center justify-center rounded-lg p-2',
        'hover:bg-muted transition',
        props.className
      )}
    />
  )
}
