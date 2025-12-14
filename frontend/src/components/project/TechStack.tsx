'use client'

import { Cpu, Database, Cloud, Wrench, CheckCircle2 } from 'lucide-react'

interface TechStackProps {
    techRecommendations: any
}

export default function TechStack({ techRecommendations }: TechStackProps) {
    if (!techRecommendations) {
        return (
            <div className="max-w-4xl mx-auto text-center py-12">
                <Cpu className="w-16 h-16 mx-auto mb-4 opacity-50 text-gray-400" />
                <p className="text-gray-500 dark:text-gray-400">Aucune recommandation disponible</p>
            </div>
        )
    }

    const { project_type, recommendations, summary } = techRecommendations

    const categories = [
        { key: 'frontend', name: 'Frontend', icon: Cpu, color: 'blue' },
        { key: 'backend', name: 'Backend', icon: Database, color: 'green' },
        { key: 'database', name: 'Base de données', icon: Database, color: 'purple' },
        { key: 'devops', name: 'DevOps', icon: Cloud, color: 'orange' },
        { key: 'tools', name: 'Outils', icon: Wrench, color: 'gray' },
    ]

    const getPriorityBadge = (priority: string) => {
        const styles = {
            'Essentiel': 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
            'Recommandé': 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
            'Requis': 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
            'Alternative': 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
            'Optionnel': 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300',
            'Utile': 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
        }
        return styles[priority as keyof typeof styles] || styles['Optionnel']
    }

    return (
        <div className="max-w-6xl mx-auto space-y-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-lg">
                <div className="flex items-center gap-3 mb-2">
                    <Cpu className="w-8 h-8" />
                    <h3 className="text-2xl font-bold">Stack Technologique Recommandé</h3>
                </div>
                <p className="text-blue-100">Type de projet: <span className="font-semibold">{project_type}</span></p>
                <p className="text-sm text-blue-100 mt-2">{summary}</p>
            </div>

            {/* Categories */}
            {categories.map((category) => {
                const techs = recommendations[category.key]
                if (!techs || techs.length === 0) return null

                const Icon = category.icon

                return (
                    <div key={category.key} className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                        <div className={`bg-${category.color}-50 dark:bg-${category.color}-900/20 p-4 border-b border-gray-200 dark:border-gray-700`}>
                            <div className="flex items-center gap-2">
                                <Icon className={`w-5 h-5 text-${category.color}-600 dark:text-${category.color}-400`} />
                                <h4 className="font-semibold text-gray-900 dark:text-white">{category.name}</h4>
                                <span className="text-xs text-gray-500 dark:text-gray-400">({techs.length} recommandations)</span>
                            </div>
                        </div>

                        <div className="p-4 space-y-4">
                            {techs.map((tech: any, idx: number) => (
                                <div key={idx} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
                                    <div className="flex items-start justify-between mb-2">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <h5 className="font-semibold text-gray-900 dark:text-white">{tech.name}</h5>
                                                <span className={`px-2 py-0.5 rounded-full text-xs ${getPriorityBadge(tech.priority)}`}>
                                                    {tech.priority}
                                                </span>
                                            </div>
                                            <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{tech.category}</p>
                                            <p className="text-sm text-gray-700 dark:text-gray-300 italic">"{tech.reason}"</p>
                                        </div>
                                    </div>

                                    {/* Pros & Cons */}
                                    <div className="grid grid-cols-2 gap-4 mt-3">
                                        <div>
                                            <p className="text-xs font-semibold text-green-600 dark:text-green-400 mb-1">✓ Avantages:</p>
                                            <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-0.5">
                                                {tech.pros?.map((pro: string, i: number) => (
                                                    <li key={i} className="flex items-start gap-1">
                                                        <span className="text-green-500">•</span>
                                                        <span>{pro}</span>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                        <div>
                                            <p className="text-xs font-semibold text-orange-600 dark:text-orange-400 mb-1">⚠ Inconvénients:</p>
                                            <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-0.5">
                                                {tech.cons?.map((con: string, i: number) => (
                                                    <li key={i} className="flex items-start gap-1">
                                                        <span className="text-orange-500">•</span>
                                                        <span>{con}</span>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )
            })}

            {/* Footer */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 text-sm text-gray-700 dark:text-gray-300">
                <CheckCircle2 className="w-5 h-5 inline mr-2 text-blue-600" />
                <strong>Note:</strong> Ces recommandations sont basées sur l'analyse de votre description de projet par notre agent IA TechAdvisor. Elles représentent les meilleures pratiques actuelles et sont adaptables selon vos contraintes spécifiques.
            </div>
        </div>
    )
}
