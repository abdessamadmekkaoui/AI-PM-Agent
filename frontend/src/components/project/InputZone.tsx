// src/components/project/InputZone.tsx
'use client'

import { useState } from 'react'
import { Sparkles, Calendar, FileText } from 'lucide-react'

interface InputZoneProps {
  onSubmit: (data: any) => void
  isLoading: boolean
}

export default function InputZone({ onSubmit, isLoading }: InputZoneProps) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    startDate: new Date().toISOString().split('T')[0]
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (formData.name && formData.description) {
      onSubmit(formData)
    }
  }

  return (
    <div className="flex-1 flex items-center justify-center p-8 overflow-y-auto">
      <div className="w-full max-w-3xl">
        
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-4">
            <Sparkles className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Créer un Nouveau Projet
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Décrivez votre projet et laissez nos agents IA créer votre planning
          </p>
        </div>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* Nom du projet */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              <FileText className="w-4 h-4 inline mr-2" />
              Nom du Projet
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Ex: Site E-commerce"
              className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              required
              disabled={isLoading}
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Description du Projet
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Décrivez votre projet en détail. Ex: Je veux créer un site e-commerce avec panier, paiement Stripe, gestion des stocks..."
              rows={8}
              className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"
              required
              disabled={isLoading}
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
              💡 Plus vous donnez de détails, plus le planning sera précis
            </p>
          </div>

          {/* Date de début */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              <Calendar className="w-4 h-4 inline mr-2" />
              Date de Début
            </label>
            <input
              type="date"
              value={formData.startDate}
              onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
              className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              required
              disabled={isLoading}
            />
          </div>

          {/* Bouton Submit */}
          <button
            type="submit"
            disabled={isLoading || !formData.name || !formData.description}
            className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Les agents travaillent...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Générer mon Projet
              </>
            )}
          </button>

          {/* Info temps */}
          {isLoading && (
            <div className="text-center text-sm text-gray-600 dark:text-gray-400">
              ⏱ Temps estimé : ~25 secondes
            </div>
          )}
        </form>

        {/* Features */}
        {!isLoading && (
          <div className="mt-12 grid grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-2xl mb-2">🤖</div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                Agent Planner
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Génère 15-20 tâches
              </p>
            </div>
            <div>
              <div className="text-2xl mb-2">📅</div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                Agent Scheduler
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Crée Gantt + Calendar
              </p>
            </div>
            <div>
              <div className="text-2xl mb-2">📝</div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                Agent Backlog
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Génère User Stories
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}