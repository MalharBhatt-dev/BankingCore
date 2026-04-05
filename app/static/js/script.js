// Theme Toggle Logic
function toggleDarkMode() {
    const html = document.documentElement;
    const body = document.body;
    
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        body.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        body.classList.remove('light-mode');
        localStorage.setItem('theme', 'dark');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Check initial theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark');
        document.body.classList.add('light-mode');
    } else {
        document.documentElement.classList.add('dark');
    }

    // Scroll Reveal Animation
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // Parallax 3D Mockup
    const mockupContainer = document.querySelector('.mockup-container');
    const mockup3d = document.querySelector('.mockup-3d');

    if (mockupContainer && mockup3d) {
        mockupContainer.addEventListener('mousemove', (e) => {
            const rect = mockupContainer.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate rotation (max 15 deg)
            const rotateX = ((y - centerY) / centerY) * -10 + 15; // default 15 + movement
            const rotateY = ((x - centerX) / centerX) * 10 - 20; // default -20 + movement
            
            mockup3d.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) rotateZ(5deg)`;
        });

        mockupContainer.addEventListener('mouseleave', () => {
             mockup3d.style.transform = `rotateX(15deg) rotateY(-20deg) rotateZ(5deg)`;
        });
    }

    // Interactive Button Click Effect (Scale and Ripple)
    const buttons = document.querySelectorAll('button:not(#themeBtn):not(.close-modal)');
    buttons.forEach(btn => {
        btn.addEventListener('mousedown', () => {
            btn.style.transform = 'scale(0.95)';
        });
        btn.addEventListener('mouseup', () => {
            btn.style.transform = 'scale(1)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
        btn.classList.add('btn-glow');
    });

    // Simulated dynamic data in mockup
    setTimeout(() => {
        const accountShimmers = document.querySelectorAll('.dynamic-account-stat')
        accountShimmers.forEach(acc => {
            acc.classList.remove('shimmer');
            acc.innerHTML = `<span class="text-sm font-bold text-gray-900 dark:text-white">•••• •••• 4562</span>`;
        })

        const balanceShimmers = document.querySelectorAll('.dynamic-balance');
        balanceShimmers.forEach(el => {
            el.classList.remove('shimmer');
            el.innerHTML = '<span class="text-3xl font-bold text-gray-900 dark:text-white">₹24,562.00</span>';
        });
    }, 2000); // 2 second mock load
});
