/**
 * API Service for HealthForce Goa
 * Connects the React UI with the FastAPI backend
 */

const API_BASE_URL = '/api';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Health Check
  async healthCheck() {
    return this.request('/health');
  }

  // Surge Analysis
  async runSurge(locationZone = 'Mumbai-West', currentTime = null) {
    return this.request('/surge/run', {
      method: 'POST',
      body: JSON.stringify({
        location_zone: locationZone,
        current_time: currentTime,
      }),
    });
  }

  async getSurgeStatus(runId) {
    return this.request(`/surge/status/${runId}`);
  }

  async listSurgeRuns() {
    return this.request('/surge/list');
  }

  async approveAction(runId, approved, modifiedPlan = null) {
    return this.request('/surge/approve', {
      method: 'POST',
      body: JSON.stringify({
        run_id: runId,
        approved,
        modified_plan: modifiedPlan,
      }),
    });
  }

  // Demo Booking
  async bookDemo(demoData) {
    return this.request('/demo/book', {
      method: 'POST',
      body: JSON.stringify(demoData),
    });
  }

  // Authentication
  async login(role, identifier, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        role,
        identifier,
        password,
      }),
    });
  }

  // Dashboard Data
  async getDashboardData(role) {
    return this.request(`/dashboard/${role}`);
  }

  // Inventory
  async getInventory(zone) {
    return this.request(`/inventory/${zone}`);
  }

  // Forecast
  async getForecast(zone) {
    return this.request(`/forecast/${zone}`);
  }
}

export const apiService = new ApiService();
export default apiService;
