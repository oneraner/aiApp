import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../Button';
import { describe, it, expect, vi } from 'vitest';

describe('Button', () => {
    it('renders correctly with children', () => {
        render(<Button>Click me</Button>);
        expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
    });

    it('handles onClick events', () => {
        const handleClick = vi.fn();
        render(<Button onClick={handleClick}>Click me</Button>);

        fireEvent.click(screen.getByRole('button', { name: /click me/i }));
        expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('respects disabled prop', () => {
        const handleClick = vi.fn();
        render(<Button disabled onClick={handleClick}>Click me</Button>);

        const button = screen.getByRole('button', { name: /click me/i });
        expect(button).toBeDisabled();

        fireEvent.click(button);
        expect(handleClick).not.toHaveBeenCalled();
    });

    it('applies variant classes', () => {
        const { container } = render(<Button variant="ghost">Ghost Button</Button>);
        expect(container.firstChild).toHaveClass('hover:bg-muted');
    });
});
