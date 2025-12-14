// frontend/src/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface ProjectData {
  name: string
  description: string
  startDate: string
}

export const api = {
  // Créer un projet
  async createProject(data: ProjectData) {
    const response = await fetch(`${API_URL}/api/projects/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: data.name,
        description: data.description,
        start_date: data.startDate,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to create project')
    }

    return response.json()
  },

  // Récupérer tous les projets
  async getProjects() {
    const response = await fetch(`${API_URL}/api/projects/`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch projects')
    }

    return response.json()
  },

  // Récupérer un projet
  async getProject(id: number) {
    const response = await fetch(`${API_URL}/api/projects/${id}`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch project')
    }

    return response.json()
  },

  // Supprimer un projet
  async deleteProject(id: number) {
    const response = await fetch(`${API_URL}/api/projects/${id}`, {
      method: 'DELETE',
    })
    
    if (!response.ok) {
      throw new Error('Failed to delete project')
    }

    return response.json()
  },

  // Mettre à jour le statut d'une tâche
  async updateTaskStatus(taskId: number, status: string) {
    const response = await fetch(`${API_URL}/api/tasks/${taskId}/status?status=${status}`, {
      method: 'PATCH',
    })
    
    if (!response.ok) {
      throw new Error('Failed to update task status')
    }

    return response.json()
  },

  // Health check
  async healthCheck() {
    const response = await fetch(`${API_URL}/health`)
    return response.json()
  }
}