import { render, screen, fireEvent } from '@testing-library/react';
import { ChatInput } from '../ChatInput';
import { describe, it, expect, vi } from 'vitest';

// Mock dependencies if necessary, but integration testing the input usually works fine without mocking child components 
// if they are simple. However, ChatInput uses TextArea and Button.
// We assume they behave like standard HTML elements or are accessible.

describe('ChatInput', () => {
    const defaultProps = {
        value: '',
        onChange: vi.fn(),
        onSubmit: vi.fn(),
    };

    it('renders correctly', () => {
        render(<ChatInput {...defaultProps} />);
        expect(screen.getByPlaceholderText(/輸入訊息/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /發送訊息/i })).toBeInTheDocument();
    });

    it('calls onChange when typing', () => {
        const handleChange = vi.fn();
        render(<ChatInput {...defaultProps} onChange={handleChange} />);

        const input = screen.getByPlaceholderText(/輸入訊息/i);
        fireEvent.change(input, { target: { value: 'Hello' } });

        expect(handleChange).toHaveBeenCalledWith('Hello');
    });

    it('handles special characters', () => {
        const handleChange = vi.fn();
        render(<ChatInput {...defaultProps} onChange={handleChange} />);

        const input = screen.getByPlaceholderText(/輸入訊息/i);
        const specialText = 'Hello @World #Test 🚀';
        fireEvent.change(input, { target: { value: specialText } });

        expect(handleChange).toHaveBeenCalledWith(specialText);
    });

    it('calls onSubmit when clicking send button with valid input', () => {
        const handleSubmit = vi.fn();
        render(<ChatInput {...defaultProps} value="Hello" onSubmit={handleSubmit} />);

        const button = screen.getByRole('button', { name: /發送訊息/i });
        expect(button).not.toBeDisabled();

        fireEvent.click(button);
        expect(handleSubmit).toHaveBeenCalledTimes(1);
    });

    it('disables send button when input is empty', () => {
        const handleSubmit = vi.fn();
        render(<ChatInput {...defaultProps} value="" onSubmit={handleSubmit} />);

        const button = screen.getByRole('button', { name: /發送訊息/i });
        expect(button).toBeDisabled();

        fireEvent.click(button);
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    it('handles Ctrl+Enter to submit', () => {
        const handleSubmit = vi.fn();
        render(<ChatInput {...defaultProps} value="Hello" onSubmit={handleSubmit} />);

        const input = screen.getByPlaceholderText(/輸入訊息/i);
        fireEvent.keyDown(input, { key: 'Enter', ctrlKey: true });

        expect(handleSubmit).toHaveBeenCalledTimes(1);
    });

    it('does not submit on Ctrl+Enter if input is empty', () => {
        const handleSubmit = vi.fn();
        render(<ChatInput {...defaultProps} value="" onSubmit={handleSubmit} />);

        const input = screen.getByPlaceholderText(/輸入訊息/i);
        fireEvent.keyDown(input, { key: 'Enter', ctrlKey: true });

        expect(handleSubmit).not.toHaveBeenCalled();
    });
});
