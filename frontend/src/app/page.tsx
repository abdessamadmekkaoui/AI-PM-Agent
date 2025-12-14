// src/app/page.tsx
'use client'

import { useState } from 'react'
import Sidebar from '@/components/layout/Sidebar'
import InputZone from '@/components/project/InputZone'
import ResultZone from '@/components/project/ResultZone'
import AgentStatus from '@/components/agents/AgentStatus'

export default function Home() {
  const [projects, setProjects] = useState<any[]>([])
  const [currentProject, setCurrentProject] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [agentStatus, setAgentStatus] = useState<{
    planner: 'idle' | 'working' | 'completed';
    scheduler: 'idle' | 'working' | 'completed';
    backlog: 'idle' | 'working' | 'completed';
  }>({
    planner: 'idle',
    scheduler: 'idle',
    backlog: 'idle'
  })

  const handleCreateProject = async (projectData: any) => {
    setIsLoading(true)
    setAgentStatus({
      planner: 'working',
      scheduler: 'idle',
      backlog: 'idle'
    })

    try {
      // Phase 1: Générer uniquement les tâches
      const response = await fetch('http://localhost:8000/api/projects/generate-tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: projectData.name,
          description: projectData.description,
          start_date: projectData.startDate,
        }),
      })

      if (!response.ok) {
        throw new Error('API Error')
      }

      const data = await response.json()

      setAgentStatus({
        planner: 'completed',
        scheduler: 'idle',
        backlog: 'idle'
      })

      // Projet avec tâches seulement
      const newProject = {
        id: data.project.id,
        name: data.project.name,
        description: data.project.description,
        startDate: data.project.start_date,
        tasks: data.tasks || [],
        userStories: [],
        ganttCode: null,
        techRecommendations: data.tech_recommendations,
        createdAt: data.project.created_at,
        phase: 'tasks_only'
      }

      setProjects(prev => [newProject, ...prev])
      setCurrentProject(newProject)
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de la création du projet. Vérifiez que le backend est lancé.')
    } finally {
      setIsLoading(false)
      setTimeout(() => {
        setAgentStatus({
          planner: 'idle',
          scheduler: 'idle',
          backlog: 'idle'
        })
      }, 1000)
    }
  }

  const handleGenerateGantt = async (projectId: number) => {
    setAgentStatus(prev => ({ ...prev, scheduler: 'working' }))

    try {
      const response = await fetch(`http://localhost:8000/api/projects/${projectId}/generate-gantt`, {
        method: 'POST',
      })

      if (!response.ok) throw new Error('API Error')

      const data = await response.json()

      console.log('✅ Gantt API Response:', data)
      console.log('📊 Gantt Code:', data.gantt_code)

      setAgentStatus(prev => ({ ...prev, scheduler: 'completed' }))

      setCurrentProject((prev: any) => ({
        ...prev,
        ganttCode: data.gantt_code,
        tasks: data.tasks,
        phase: prev.userStories?.length > 0 ? 'complete' : 'tasks_and_gantt'
      }))

      setProjects(prevProjects =>
        prevProjects.map(p =>
          p.id === projectId
            ? { ...p, ganttCode: data.gantt_code, tasks: data.tasks }
            : p
        )
      )
    } catch (error) {
      console.error('Erreur Gantt:', error)
      alert('Erreur génération Gantt')
    }
  }

  const handleGenerateBacklog = async (projectId: number) => {
    setAgentStatus(prev => ({ ...prev, backlog: 'working' }))

    try {
      const response = await fetch(`http://localhost:8000/api/projects/${projectId}/generate-backlog`, {
        method: 'POST',
      })

      if (!response.ok) throw new Error('API Error')

      const data = await response.json()

      setAgentStatus(prev => ({ ...prev, backlog: 'completed' }))

      setCurrentProject((prev: any) => ({
        ...prev,
        userStories: data.user_stories,
        phase: prev.ganttCode ? 'complete' : 'tasks_and_backlog'
      }))

      setProjects(prevProjects =>
        prevProjects.map(p =>
          p.id === projectId
            ? { ...p, userStories: data.user_stories }
            : p
        )
      )
    } catch (error) {
      console.error('Erreur Backlog:', error)
      alert('Erreur génération Backlog')
    }
  }

  const handleTaskStatusUpdate = async (taskId: number, newStatus: string) => {
    try {
      // Optimistic update
      setCurrentProject((prev: any) => ({
        ...prev,
        tasks: prev.tasks.map((t: any) =>
          t.id === taskId ? { ...t, status: newStatus } : t
        )
      }))

      setProjects(prevProjects =>
        prevProjects.map(p =>
          p.id === currentProject.id
            ? {
              ...p,
              tasks: p.tasks.map((t: any) =>
                t.id === taskId ? { ...t, status: newStatus } : t
              )
            }
            : p
        )
      )

      // API Call
      const response = await fetch(`http://localhost:8000/api/projects/tasks/${taskId}/status?status=${newStatus}`, {
        method: 'PATCH',
      })

      if (!response.ok) {
        throw new Error('Failed to update task')
      }
    } catch (error) {
      console.error('Error updating task:', error)
      alert('Erreur lors de la mise à jour de la tâche')
      // Revert would be nice here but keeping it simple
    }
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar
        projects={projects}
        currentProject={currentProject}
        onSelectProject={setCurrentProject}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        {isLoading && (
          <AgentStatus status={agentStatus} />
        )}

        {!currentProject ? (
          <InputZone
            onSubmit={handleCreateProject}
            isLoading={isLoading}
          />
        ) : (
          <ResultZone
            project={currentProject}
            onBack={() => setCurrentProject(null)}
            onGenerateGantt={handleGenerateGantt}
            onGenerateBacklog={handleGenerateBacklog}
            onTaskStatusChange={handleTaskStatusUpdate}
          />
        )}
      </div>
    </div>
  )
}