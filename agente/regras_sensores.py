sensores = {
    'CAF-98-001': {
        'consumo_kw':{
            'critico': 6,
            'atencao': 5,
            'unidade_medida': 'kw'
        },

        'temperatura_c':{
            'critico': 85, 
            'atencao': 82.5,
            'unidade_medida': 'C'
        },

        'vibracao_mm_s': {
            'critico': 8,
            'atencao': 6,
            'unidade_medida': 'mm/s'
        },

    },

    'CAF-22-001': {
        'consumo_kw':{
            'critico': 2,
            'atencao': 1.5,
            'unidade_medida': 'kw'
        },

        'temperatura_c':{
            'critico': 80,
            'atencao': 70,
            'unidade_medida': 'C'
        },
    },

    'ROUTER-001': {
        'potencia_kw': {
            'critico': 4,
            'atencao': 3,
            'unidade_medida': 'kw'
        },

        'spindle_entrada_hz':{
            'critico': 70,
            'atencao': 60,
            'unidade_medida': 'hz'
        },

        'spindle_saida_hz':{
            'critico': 500,
            'atencao': 450,
            'unidade_medida': 'hz' 
        },
    },

    'ROMO-ES40-001': {
        'potencia_kw':{
            'critico': 18,
            'atencao': 17,
            'unidade_medida': 'kw'
        },

        'spindle_carga_kw': {
            'critico': 18,
            'atencao': 17,
            'unidade_medida': 'kw'
        },

        'velocidade_rpm':{
            'critico': 2600,
            'atencao': 2450,
            'unidade_medida': 'rpm'
        }
    }
}
