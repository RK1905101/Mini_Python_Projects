document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const habitsContainer = document.querySelector('.habits-container');
    const addHabitBtn = document.getElementById('addHabitBtn');
    const habitModal = document.getElementById('habitModal');
    const closeBtn = document.querySelector('.close-btn');
    const saveHabitBtn = document.getElementById('saveHabitBtn');
    const cancelHabitBtn = document.getElementById('cancelHabitBtn');
    const habitInput = document.getElementById('habitInput');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const themeToggle = document.getElementById('themeToggle');

    // Load habits from localStorage or use default
    let habits = JSON.parse(localStorage.getItem('habits')) || [
        { id: 1, name: 'Drink 8 glasses of water', completed: false, streak: 0, lastCompleted: null },
        { id: 2, name: '30 minutes of exercise', completed: false, streak: 0, lastCompleted: null },
        { id: 3, name: 'Read 10 pages', completed: false, streak: 0, lastCompleted: null }
    ];

    // Initialize the app
    function init() {
        setupThemeToggle();
        renderHabits();
        updateProgress();
        setupEventListeners();
    }

    // Set up all event listeners
    function setupEventListeners() {
        addHabitBtn.addEventListener('click', openModal);
        closeBtn.addEventListener('click', closeModal);
        cancelHabitBtn.addEventListener('click', closeModal);
        saveHabitBtn.addEventListener('click', saveHabit);
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === habitModal) {
                closeModal();
            }
        });
        
        // Allow Enter key to save habit
        habitInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                saveHabit();
            }
        });
    }

    // Theme Toggle Functionality
    function setupThemeToggle() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Set initial theme
        if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && prefersDark)) {
            document.body.classList.add('dark-mode');
            themeToggle.checked = true;
        }
        
        themeToggle.addEventListener('change', toggleTheme);
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        
        // Animate toggle
        anime({
            targets: '.slider',
            backgroundColor: document.body.classList.contains('dark-mode') ? 
                [getComputedStyle(document.documentElement).getPropertyValue('--secondary'), getComputedStyle(document.documentElement).getPropertyValue('--primary')] : 
                ['#ccc', getComputedStyle(document.documentElement).getPropertyValue('--primary')],
            duration: 300
        });
    }

    // Modal Functions
    function openModal() {
        habitModal.style.display = 'flex';
        habitInput.value = '';
        habitInput.focus();
        
        // Animate modal open
        anime({
            targets: '.modal-content',
            scale: [0.9, 1],
            opacity: [0, 1],
            duration: 300,
            easing: 'easeOutBack'
        });
    }

    function closeModal() {
        anime({
            targets: '.modal-content',
            scale: 0.9,
            opacity: 0,
            duration: 200,
            easing: 'easeInOutQuad',
            complete: () => {
                habitModal.style.display = 'none';
            }
        });
    }

    function saveHabit() {
        const habitName = habitInput.value.trim();
        
        if (habitName) {
            const newHabit = {
                id: Date.now(),
                name: habitName,
                completed: false,
                streak: 0,
                lastCompleted: null
            };
            
            habits.unshift(newHabit);
            saveHabits();
            renderHabits();
            updateProgress();
            closeModal();
            
            // Show success animation
            anime({
                targets: addHabitBtn,
                backgroundColor: ['#00b894', '#6c5ce7'],
                duration: 1000,
                easing: 'easeOutExpo'
            });
        } else {
            // Show error animation
            anime({
                targets: habitInput,
                borderColor: [getComputedStyle(document.documentElement).getPropertyValue('--danger'), '#ddd'],
                duration: 1000,
                easing: 'easeOutExpo'
            });
        }
    }

    // Render habits to the DOM
    function renderHabits() {
        habitsContainer.innerHTML = '';
        
        if (habits.length === 0) {
            habitsContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-clipboard-list"></i>
                    <p>No habits yet. Add your first habit!</p>
                </div>
            `;
            return;
        }
        
        habits.forEach(habit => {
            const habitElement = document.createElement('div');
            habitElement.className = `habit-item ${habit.completed ? 'completed' : ''}`;
            habitElement.dataset.id = habit.id;
            
            habitElement.innerHTML = `
                <span class="habit-name">${habit.name}</span>
                <div class="habit-actions">
                    ${habit.streak > 0 ? `
                        <div class="streak-counter ${habit.streak > 0 ? 'active' : ''}">
                            <i class="fas fa-fire"></i>
                            <span>${habit.streak} day${habit.streak !== 1 ? 's' : ''}</span>
                        </div>
                    ` : ''}
                    <div class="habit-check">
                        <i class="fas fa-check"></i>
                    </div>
                    <div class="delete-habit">
                        <i class="fas fa-trash"></i>
                    </div>
                </div>
            `;
            
            habitsContainer.appendChild(habitElement);
            
            // Add click event for completion toggle
            const checkBtn = habitElement.querySelector('.habit-check');
            checkBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleHabitCompletion(habit.id);
            });
            
            // Add click event for deletion
            const deleteBtn = habitElement.querySelector('.delete-habit');
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                deleteHabit(habit.id);
            });
            
            // Add animation on render
            anime({
                targets: habitElement,
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 600,
                delay: habits.indexOf(habit) * 100,
                easing: 'easeOutExpo'
            });
        });
    }

    // Toggle habit completion status
    function toggleHabitCompletion(id) {
        const habitIndex = habits.findIndex(habit => habit.id === id);
        if (habitIndex !== -1) {
            const wasCompleted = habits[habitIndex].completed;
            habits[habitIndex].completed = !wasCompleted;
            
            const habitElement = document.querySelector(`.habit-item[data-id="${id}"]`);
            
            if (habits[habitIndex].completed) {
                // Update streak when completing
                updateStreak(id);
                
                anime({
                    targets: habitElement,
                    backgroundColor: 'rgba(0, 184, 148, 0.1)',
                    borderLeftColor: '#00b894',
                    duration: 500,
                    easing: 'easeOutExpo'
                });
                
                createConfetti(habitElement);
                
                anime({
                    targets: habitElement.querySelector('.habit-check'),
                    scale: [1, 1.2, 1],
                    duration: 300,
                    easing: 'easeOutBack'
                });
            } else {
                // Visual feedback when unchecking
                anime({
                    targets: habitElement,
                    backgroundColor: document.body.classList.contains('dark-mode') ? '#2d2d2d' : '#ffffff',
                    borderLeftColor: '#ddd',
                    duration: 300,
                    easing: 'easeOutExpo'
                });
            }
            
            habitElement.classList.toggle('completed');
            saveHabits();
            renderHabits(); // Re-render to update streak counter
            updateProgress();
        }
    }

    // Streak Tracking Functions
    function updateStreak(habitId) {
        const habitIndex = habits.findIndex(habit => habit.id === habitId);
        if (habitIndex === -1) return;
        
        const habit = habits[habitIndex];
        const today = new Date().toDateString();
        
        if (habit.completed) {
            // If habit was already completed today, do nothing
            if (habit.lastCompleted === today) return;
            
            // If last completed was yesterday, increment streak
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            
            if (habit.lastCompleted === yesterday.toDateString() || habit.streak === 0) {
                habit.streak++;
            } else if (habit.lastCompleted !== today) {
                // Reset streak if broken
                habit.streak = 1;
            }
            
            habit.lastCompleted = today;
        }
    }

    // Delete a habit
    function deleteHabit(id) {
        const habitIndex = habits.findIndex(habit => habit.id === id);
        if (habitIndex !== -1) {
            const habitElement = document.querySelector(`.habit-item[data-id="${id}"]`);
            
            // Animate deletion
            anime({
                targets: habitElement,
                opacity: 0,
                translateX: 100,
                duration: 400,
                easing: 'easeInExpo',
                complete: () => {
                    habits.splice(habitIndex, 1);
                    saveHabits();
                    renderHabits();
                    updateProgress();
                }
            });
        }
    }

    // Update progress bar
    function updateProgress() {
        const completedCount = habits.filter(habit => habit.completed).length;
        const totalCount = habits.length;
        const percentage = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;
        
        // Animate progress bar
        anime({
            targets: progressBar,
            width: `${percentage}%`,
            duration: 800,
            easing: 'easeOutExpo'
        });
        
        // Animate progress text
        anime({
            targets: progressText,
            innerHTML: [progressText.textContent, `${percentage}%`],
            round: 1,
            duration: 800,
            easing: 'easeOutExpo'
        });
        
        // If all habits are completed, celebrate!
        if (percentage === 100 && totalCount > 0) {
            celebrateCompletion();
        }
    }

    // Create confetti effect
    function createConfetti(element) {
        const rect = element.getBoundingClientRect();
        const colors = ['#6c5ce7', '#00b894', '#0984e3', '#fdcb6e', '#e17055'];
        
        for (let i = 0; i < 20; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            document.body.appendChild(confetti);
            
            anime({
                targets: confetti,
                left: rect.left + (rect.width / 2) + 'px',
                top: rect.top + 'px',
                translateX: () => anime.random(-100, 100),
                translateY: () => anime.random(-100, -200),
                rotate: () => anime.random(0, 360),
                opacity: [1, 0],
                duration: 1500,
                easing: 'easeOutExpo',
                complete: () => confetti.remove()
            });
        }
    }

    // Celebrate when all habits are completed
    function celebrateCompletion() {
        anime({
            targets: '.container',
            scale: [1, 1.05, 1],
            duration: 1000,
            easing: 'easeOutElastic'
        });
        
        // Fireworks animation
        const fireworks = () => {
            const colors = ['#6c5ce7', '#00b894', '#0984e3', '#fdcb6e', '#e17055'];
            const container = document.querySelector('.container');
            const rect = container.getBoundingClientRect();
            
            for (let i = 0; i < 5; i++) {
                const particle = document.createElement('div');
                particle.className = 'confetti';
                particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                particle.style.width = '6px';
                particle.style.height = '6px';
                particle.style.borderRadius = '50%';
                document.body.appendChild(particle);
                
                anime({
                    targets: particle,
                    left: rect.left + (rect.width / 2) + 'px',
                    top: rect.top + (rect.height / 2) + 'px',
                    translateX: () => anime.random(-150, 150),
                    translateY: () => anime.random(-150, 150),
                    opacity: [1, 0],
                    duration: 1500,
                    easing: 'easeOutExpo',
                    complete: () => particle.remove()
                });
            }
        };
        
        // Run fireworks 3 times with delay
        fireworks();
        setTimeout(fireworks, 300);
        setTimeout(fireworks, 600);
    }

    // Save habits to localStorage
    function saveHabits() {
        localStorage.setItem('habits', JSON.stringify(habits));
    }

    // Initialize the app
    init();
});