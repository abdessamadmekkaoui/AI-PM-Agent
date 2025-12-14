// src/components/layout/Sidebar.tsx
'use client'

import { FolderKanban, Plus, Calendar, Settings } from 'lucide-react'

interface SidebarProps {
  projects: any[]
  currentProject: any
  onSelectProject: (project: any) => void
}

export default function Sidebar({ projects, currentProject, onSelectProject }: SidebarProps) {
  return (
    <aside className="w-72 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-2 mb-4">
          <FolderKanban className="w-6 h-6 text-blue-600" />
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
            AI PM Agent
          </h1>
        </div>
        
        <button 
          onClick={() => onSelectProject(null)}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Nouveau Projet
        </button>
      </div>

      {/* Liste des projets */}
      <div className="flex-1 overflow-y-auto p-4">
        <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
          Projets Récents
        </h2>
        
        {projects.length === 0 ? (
          <div className="text-center py-8 text-gray-400 dark:text-gray-500">
            <FolderKanban className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p className="text-sm">Aucun projet créé</p>
            <p className="text-xs mt-1">Créez votre premier projet</p>
          </div>
        ) : (
          <div className="space-y-2">
            {projects.map((project) => (
              <button
                key={project.id}
                onClick={() => onSelectProject(project)}
                className={`w-full text-left p-3 rounded-lg transition-colors ${
                  currentProject?.id === project.id
                    ? 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700/50'
                }`}
              >
                <div className="flex items-start justify-between mb-1">
                  <h3 className="font-medium text-gray-900 dark:text-white text-sm line-clamp-1">
                    {project.name}
                  </h3>
                  <span className="text-xs text-gray-400">
                    {new Date(project.createdAt).toLocaleDateString('fr-FR', {
                      day: '2-digit',
                      month: 'short'
                    })}
                  </span>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2">
                  {project.description}
                </p>
                <div className="flex items-center gap-3 mt-2 text-xs text-gray-400">
                  <span>{project.tasks?.length || 0} tâches</span>
                  <span>•</span>
                  <span>{project.userStories?.length || 0} stories</span>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <button className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <Settings className="w-4 h-4" />
          Paramètres
        </button>
      </div>
    </aside>
  )
}