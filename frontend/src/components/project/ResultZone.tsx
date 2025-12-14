// src/components/project/ResultZone.tsx
'use client'

import { useState } from 'react'
import { ArrowLeft, CheckCircle2, Clock, Calendar, FileText, Check, Cpu } from 'lucide-react'
import GanttDiagram from '@/components/visualizations/GanttDiagram'
import TechStack from './TechStack'

interface ResultZoneProps {
  project: any
  onBack: () => void
  onGenerateGantt?: (projectId: number) => void
  onGenerateBacklog?: (projectId: number) => void
  onTaskStatusChange?: (taskId: number, newStatus: string) => void
}

export default function ResultZone({ project, onBack, onGenerateGantt, onGenerateBacklog, onTaskStatusChange }: ResultZoneProps) {
  const [activeTab, setActiveTab] = useState<'tasks' | 'gantt' | 'techstack' | 'backlog'>('tasks')

  return (
    <div className="flex-1 flex flex-col overflow-hidden">

      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                {project.name}
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Créé le {new Date(project.createdAt).toLocaleDateString('fr-FR')}
              </p>
            </div>
          </div>

          {/* Stats rapides */}
          <div className="flex items-center gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {project.tasks?.length || 0}
              </div>
              <div className="text-xs text-gray-500">Tâches</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {project.userStories?.length || 0}
              </div>
              <div className="text-xs text-gray-500">Stories</div>
            </div>
          </div>

          {/* Action Buttons for Phases */}
          {(project.phase === 'tasks_only' || !project.ganttCode || !project.userStories?.length) && (
            <div className="flex items-center gap-3">
              {!project.ganttCode && onGenerateGantt && (
                <button
                  onClick={() => onGenerateGantt(project.id)}
                  className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                >
                  <Calendar className="w-4 h-4" />
                  Générer Gantt
                </button>
              )}
              {!project.userStories?.length && onGenerateBacklog && (
                <button
                  onClick={() => onGenerateBacklog(project.id)}
                  className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
                >
                  <FileText className="w-4 h-4" />
                  Générer Backlog
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6">
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('tasks')}
            className={`px-4 py-3 font-medium transition-colors relative ${activeTab === 'tasks'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
          >
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              Tâches
            </div>
            {activeTab === 'tasks' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('gantt')}
            className={`px-4 py-3 font-medium transition-colors relative ${activeTab === 'gantt'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
          >
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Gantt
            </div>
            {activeTab === 'gantt' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('backlog')}
            className={`px-4 py-3 font-medium transition-colors relative ${activeTab === 'backlog'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
          >
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Backlog
            </div>
            {activeTab === 'backlog' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('techstack')}
            className={`px-4 py-3 font-medium transition-colors relative ${activeTab === 'techstack'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
          >
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4" />
              Tech Stack
            </div>
            {activeTab === 'techstack' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
            )}
          </button>
        </div>
      </div>

      {/* Contenu */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-900">

        {/* TAB: TÂCHES */}
        {activeTab === 'tasks' && (
          <div className="max-w-4xl mx-auto space-y-3">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Liste des Tâches ({project.tasks?.length || 0})
              </h3>
            </div>

            {project.tasks?.map((task: any) => (
              <div
                key={task.id}
                className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start gap-3">
                  {/* Checkbox */}
                  <button
                    onClick={() => {
                      const newStatus = task.status === 'done' ? 'todo' : 'done'
                      if (onTaskStatusChange) {
                        onTaskStatusChange(task.id, newStatus)
                      }
                    }}
                    className={`flex-shrink-0 mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${task.status === 'done'
                      ? 'bg-green-600 border-green-600'
                      : 'border-gray-300 dark:border-gray-600 hover:border-green-500'
                      }`}
                  >
                    {task.status === 'done' && (
                      <Check className="w-3 h-3 text-white" strokeWidth={3} />
                    )}
                  </button>

                  <div className="flex-1">
                    <h4 className={`font-medium mb-1 ${task.status === 'done'
                      ? 'text-gray-500 dark:text-gray-400 line-through'
                      : 'text-gray-900 dark:text-white'
                      }`}>
                      {task.title}
                    </h4>
                    <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {task.duration_days} jours
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs ${task.status === 'done'
                        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                        : task.status === 'in-progress'
                          ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                          : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                        }`}>
                        {task.status === 'todo' ? 'À faire' :
                          task.status === 'in-progress' ? 'En cours' : 'Terminé'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB: GANTT */}
        {activeTab === 'gantt' && (
          <div className="max-w-6xl mx-auto space-y-4">
            {project.ganttCode ? (
              <>
                <GanttDiagram ganttCode={project.ganttCode} projectName={project.name} />

                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                  <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                    💡 Le diagramme ne s'affiche pas? Visualisez-le sur Mermaid Live:
                  </p>
                  <a
                    href="https://mermaid.live"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded hover:bg-blue-700 transition-colors"
                  >
                    <Calendar className="w-4 h-4" />
                    Ouvrir sur Mermaid.live
                  </a>

                  <details className="mt-4">
                    <summary className="cursor-pointer text-sm text-blue-600 dark:text-blue-400 hover:underline">
                      Voir le code Mermaid
                    </summary>
                    <pre className="mt-2 text-xs bg-gray-50 dark:bg-gray-900 p-3 rounded border border-gray-200 dark:border-gray-700 overflow-x-auto">
                      {project.ganttCode}
                    </pre>
                  </details>
                </div>
              </>
            ) : (
              <div className="bg-white dark:bg-gray-800 p-8 rounded-lg border border-gray-200 dark:border-gray-700 text-center">
                <Calendar className="w-16 h-16 mx-auto mb-4 opacity-50 text-gray-400" />
                <p className="text-gray-500 dark:text-gray-400">Aucun diagramme Gantt disponible</p>
                <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
                  Cliquez sur "Générer Gantt" pour créer le diagramme
                </p>
              </div>
            )}
          </div>
        )}

        {/* TAB: BACKLOG */}
        {activeTab === 'backlog' && (
          <div className="max-w-4xl mx-auto space-y-3">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                User Stories ({project.userStories?.length || 0})
              </h3>
            </div>

            {project.userStories?.map((story: any) => (
              <div
                key={story.id}
                className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-gray-900 dark:text-white flex-1">
                    {story.title}
                  </h4>
                  <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 text-xs rounded-full">
                    {story.points} pts
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded text-xs ${story.priority === 'Must Have'
                    ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                    : story.priority === 'Should Have'
                      ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
                      : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                    }`}>
                    {story.priority}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB: TECH STACK */}
        {activeTab === 'techstack' && (
          <TechStack techRecommendations={project.techRecommendations} />
        )}
      </div>
    </div>
  )
}