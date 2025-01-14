import { Component, OnInit, OnDestroy } from '@angular/core';
import { LoginComponent } from '../login/login.component';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { trigger, state, style, animate, transition } from '@angular/animations';
import axios from 'axios';

interface CryptoCurrency {
    name: string;
    symbol: string;
    price: string;
    imgSrc: string;
    trend: number;
    trendClass: string;
}

interface FaqItem {
    question: string;
    answer: string;
    isOpen: boolean;
}

@Component({
    selector: 'app-homet',
    standalone: true,
    imports: [LoginComponent, RouterModule, CommonModule],
    templateUrl: './homet.component.html',
    styleUrls: ['./homet.component.scss'],
    animations: [
        trigger('expandCollapse', [
            state('collapsed', style({
                height: '0',
                opacity: 0,
                padding: 0
            })),
            state('expanded', style({
                height: '*', // Prend la hauteur de son contenu
                opacity: 1,
                padding: '*',
            })),
            transition('collapsed <=> expanded', [
                animate('300ms ease-in-out'),
            ]),
        ])
    ]
})
export class HometComponent implements OnInit, OnDestroy {
    isLightMode = true;
    cryptocurrencies: CryptoCurrency[] = [];
    faqItems: FaqItem[] = [
        {
            question: 'What is Cryptocurrency?',
            answer: 'Cryptocurrency is a digital or virtual currency secured by cryptography, making it nearly impossible to counterfeit. It operates on decentralized networks based on blockchain technology.',
            isOpen: false
        },
        {
            question: 'How do I start investing?',
            answer: 'Begin by choosing a reputable cryptocurrency exchange, creating an account, and connecting your payment method. Start with small investments while learning the market dynamics.',
            isOpen: false
        },
        {
            question: 'Is cryptocurrency safe?',
            answer: 'While blockchain technology is secure, cryptocurrency investments carry risks due to market volatility. Always research thoroughly and never invest more than you can afford to lose.',
            isOpen: false
        }
    ];

    private intervalId: any; // Variable pour stocker l'ID de l'intervalle

    ngOnInit(): void {
        this.loadTheme();
        this.loadCryptocurrencies();
        
        // Recharger les données toutes les 3 secondes
        this.intervalId = setInterval(() => {
            this.loadCryptocurrencies();
        }, 3000); // 3000 ms = 3 secondes
    }

    ngOnDestroy(): void {
        // Nettoyer l'intervalle lorsque le composant est détruit
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }

    toggleFaq(item: FaqItem): void {
        item.isOpen = !item.isOpen;
    }

    onLogin(): void {
        alert('Login button clicked!');
        // Logique de connexion ici
    }

    toggleTheme(): void {
        this.isLightMode = !this.isLightMode;
        localStorage.setItem('theme', this.isLightMode ? 'light' : 'dark');
    }

    loadTheme(): void {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            this.isLightMode = false;
        } else {
            this.isLightMode = true;
        }
    }

    // Method to fetch data from Binance API using Axios
    async loadCryptocurrencies(): Promise<void> {
        const symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT'];
        const images = ['bitcoin', 'ethereum', 'binance-coin', 'cardano'];
        const apiUrl = 'https://api.binance.com/api/v3/ticker/24hr?symbol=';
    
        const requests = symbols.map((symbol, index) =>
            //recover  last price price change percent 
            axios.get<any>(apiUrl + symbol).then(response => {
                // Formater le prix avec des virgules
                const formattedPrice = new Intl.NumberFormat('en-US', {
                    style: 'decimal',
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }).format(parseFloat(response.data.lastPrice));
    
                return {
                    name: symbol.substring(0, 3),
                    symbol: symbol.substring(0, 3),
                    price: `$${formattedPrice}`, // Prix formaté
                    imgSrc: `https://cryptologos.cc/logos/${images[index]}-${symbol.substring(0, 3).toLowerCase()}-logo.png`,
                    trend: parseFloat(response.data.priceChangePercent),
                    trendClass: parseFloat(response.data.priceChangePercent) > 0 ? 'positive' : 'negative'
                };
            }).catch(error => {
                console.error('Erreur lors de la récupération des données :', error);
                return null;
            })
        );
    
        const results = await Promise.all(requests);
    
        // Filter out null results and assign them to cryptocurrencies
        this.cryptocurrencies = results.filter((result): result is CryptoCurrency => result !== null);
    }    
    
}
