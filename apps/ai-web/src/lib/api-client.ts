// src/lib/api-client.ts

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface APIError {
  detail?: string | { error?: string; message?: string };
  status?: number;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: APIError = await response.json().catch(() => ({
      detail: `HTTP ${response.status}: ${response.statusText}`,
      status: response.status,
    }));

    // Extract error message
    let errorMessage = "發生錯誤";
    if (typeof error.detail === "string") {
      errorMessage = error.detail;
    } else if (error.detail && typeof error.detail === "object") {
      errorMessage = error.detail.message || error.detail.error || errorMessage;
    }

    throw new Error(errorMessage);
  }

  return response.json();
}

export const apiClient = {
  // AI endpoints
  async triggerAI(params: {
    model: string;
    contents: Array<{ type: string; content: string }>;
    conversationId?: string;
  }): Promise<{ job_id: string; conversation_id: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/ai/trigger`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: params.model,
        contents: params.contents,
        conversation_id: params.conversationId,
      }),
    });
    return handleResponse(response);
  },

  // Stream endpoint returns EventSource for SSE
  streamResponse(jobId: string): EventSource {
    return new EventSource(`${API_BASE_URL}/api/v1/ai/stream/${jobId}`);
  },

  // Models
  async getModels(): Promise<
    Array<{ name: string; provider: string; capabilities: string[] }>
  > {
    const response = await fetch(`${API_BASE_URL}/api/v1/models/`);
    return handleResponse(response);
  },

  // Conversations
  async getConversations(): Promise<
    Array<{
      id: string;
      created_at: string;
      updated_at: string;
      message_count: number;
    }>
  > {
    const response = await fetch(`${API_BASE_URL}/api/v1/conversations/`);
    return handleResponse(response);
  },

  async getConversation(id: string): Promise<{
    id: string;
    created_at: string;
    updated_at: string;
    messages: Array<{
      id: string;
      role: string;
      content: string;
      model_used: string | null;
      created_at: string;
    }>;
  }> {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/conversations/${id}`,
    );
    return handleResponse(response);
  },

  async deleteConversation(id: string): Promise<{ success: boolean }> {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/conversations/${id}`,
      { method: "DELETE" },
    );
    return handleResponse(response);
  },

  // Admin endpoints
  async resetRateLimit(): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/admin/reset-limit`, {
      method: "POST",
    });
    return handleResponse(response);
  },

  async getRateLimitStatus(): Promise<{
    used?: number;
    remaining?: number;
    limit?: number;
    reset_time?: string;
  }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/admin/limit-status`);
    return handleResponse(response);
  },
};
