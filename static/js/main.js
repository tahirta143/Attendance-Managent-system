// Loader handling
function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader && !loader.classList.contains('fade-out')) {
        setTimeout(() => {
            loader.classList.add('fade-out');
            setTimeout(() => {
                loader.style.display = 'none';
            }, 500);
        }, 300);
    }
}

if (document.readyState === 'complete') {
    hideLoader();
} else {
    window.addEventListener('load', hideLoader);
}

// Fallback: Force hide loader after 3 seconds if it's still stuck
setTimeout(hideLoader, 3000);

// Sidebar Toggle
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleBtn');
const mainContent = document.getElementById('mainContent');

if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');

        gsap.to(sidebar, {
            duration: 0.3,
            ease: 'power2.inOut'
        });
    });
}

// Animate page content on load
document.addEventListener('DOMContentLoaded', () => {
    // Fade in content
    gsap.to('.content', {
        duration: 0.4,
        opacity: 1,
        ease: 'power1.inOut'
    });

    // Animate table rows
    const tableRows = document.querySelectorAll('tbody tr');
    if (tableRows.length > 0) {
        gsap.from(tableRows, {
            duration: 0.4,
            opacity: 0,
            y: 10,
            stagger: 0.05,
            ease: 'power2.out'
        });
    }

    // Animate form
    const formGroups = document.querySelectorAll('.form-group');
    if (formGroups.length > 0) {
        gsap.from(formGroups, {
            duration: 0.5,
            opacity: 0,
            x: -20,
            stagger: 0.1,
            ease: 'power2.out'
        });
    }
});

// Button hover effects
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mouseenter', function () {
        gsap.to(this, {
            duration: 0.3,
            scale: 1.05,
            ease: 'power2.out'
        });
    });

    btn.addEventListener('mouseleave', function () {
        gsap.to(this, {
            duration: 0.3,
            scale: 1,
            ease: 'power2.out'
        });
    });
});

// Card hover effects
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function () {
        gsap.to(this, {
            duration: 0.3,
            y: -8,
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.2)',
            ease: 'power2.out'
        });
    });

    card.addEventListener('mouseleave', function () {
        gsap.to(this, {
            duration: 0.3,
            y: 0,
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            ease: 'power2.out'
        });
    });
});

// Auto-hide alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        gsap.to(alert, {
            duration: 0.5,
            opacity: 0,
            height: 0,
            marginBottom: 0,
            ease: 'power2.inOut',
            onComplete: () => alert.remove()
        });
    });
}, 5000);

// Confirm delete actions
document.querySelectorAll('.action-btn-delete').forEach(btn => {
    btn.addEventListener('click', function (e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            gsap.to(window, {
                duration: 0.8,
                scrollTo: target,
                ease: 'power2.inOut'
            });
        }
    });
});
