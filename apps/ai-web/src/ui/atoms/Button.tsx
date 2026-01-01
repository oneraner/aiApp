import { cn } from '@/lib/cn'

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'ghost'
}

export function Button({
  className,
  variant = 'primary',
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-xl text-sm font-medium transition',
        'disabled:opacity-50 disabled:pointer-events-none',
        variant === 'primary' &&
          'bg-primary text-primary-foreground hover:bg-primary/90',
        variant === 'ghost' &&
          'hover:bg-muted text-foreground',
        className
      )}
      {...props}
    />
  )
}
