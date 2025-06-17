document.addEventListener('DOMContentLoaded', function() {
    // Initialize accordion menu behavior
    initializeAccordionMenu();
    
    // Initialize all charts
    initCharts();
    
    // Set up event listeners with proper AJAX handling
    setupEventListeners();
    

    // Initialize call data dashboard when the page loads
    console.log('Initializing Call Data Dashboard...');
    initializeCallCharts();
    loadCallData();
    setupCallEventListeners();
    startRealTimeCallUpdates();

    // Initialize case management dashboard when the page loads
    console.log('Initializing Case Management Dashboard...');
    initializeCaseCharts();
    loadCaseData();
    setupCaseEventListeners();
    startRealTimeCaseUpdates();

    // Initialize contacts dashboard when the page loads
    console.log('Initializing Contacts Dashboard...');
    initializeContactsDashboard();

    // User Roles Management JavaScript
    renderPermissions();
    // Check if users exist and update counts
    const userItems = document.querySelectorAll('.user-item[data-user-id]');
    if (userItems.length > 0) {
        updateRoleCounts();
    }

    // Initialize theme on page load
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    applyTheme(savedTheme);
    
    // Update button text and icon
    const themeBtn = document.querySelector('.theme-btn span');
    const themeIcon = document.querySelector('.theme-btn .nav-icon');
    
    if (themeBtn) {
        themeBtn.textContent = savedTheme === 'dark' ? 'Light Theme' : 'Dark Theme';
    }
    
    if (themeIcon) {
        themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    }
});

// Accordion menu functionality - ensures only one dropdown is open at a time
function initializeAccordionMenu() {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle[href^="#"]');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetCollapse = document.querySelector(targetId);
            
            if (!targetCollapse) {
                console.warn('Target collapse element not found:', targetId);
                return;
            }
            
            // Close all other open dropdowns
            const allCollapses = document.querySelectorAll('.collapse.show');
            allCollapses.forEach(collapse => {
                if (collapse !== targetCollapse) {
                    // Remove show class and update aria-expanded
                    collapse.classList.remove('show');
                    const correspondingToggle = document.querySelector(`[href="#${collapse.id}"]`);
                    if (correspondingToggle) {
                        correspondingToggle.setAttribute('aria-expanded', 'false');
                        // Remove active styling
                        correspondingToggle.classList.remove('active');
                    }
                }
            });
            
            // Toggle the clicked dropdown
            const isCurrentlyOpen = targetCollapse.classList.contains('show');
            
            if (isCurrentlyOpen) {
                // Close the dropdown
                targetCollapse.classList.remove('show');
                this.setAttribute('aria-expanded', 'false');
                this.classList.remove('active');
            } else {
                // Open the dropdown
                targetCollapse.classList.add('show');
                this.setAttribute('aria-expanded', 'true');
                this.classList.add('active');
            }
            
            // Add a small delay to ensure smooth animation
            setTimeout(() => {
                // Scroll the sidebar if needed to show the opened dropdown
                if (!isCurrentlyOpen && targetCollapse) {
                    const sidebar = document.querySelector('.sidebar');
                    const toggleRect = this.getBoundingClientRect();
                    const sidebarRect = sidebar.getBoundingClientRect();
                    
                    // Check if the dropdown extends below the visible area
                    const dropdownBottom = toggleRect.bottom + targetCollapse.offsetHeight;
                    const sidebarBottom = sidebarRect.bottom;
                    
                    if (dropdownBottom > sidebarBottom) {
                        sidebar.scrollTop += dropdownBottom - sidebarBottom + 20; // Add some padding
                    }
                }
            }, 100);
        });
    });
    
    // Handle clicks outside dropdowns to close them (optional)
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.sidebar')) {
            const openDropdowns = document.querySelectorAll('.collapse.show');
            openDropdowns.forEach(dropdown => {
                dropdown.classList.remove('show');
                const toggle = document.querySelector(`[href="#${dropdown.id}"]`);
                if (toggle) {
                    toggle.setAttribute('aria-expanded', 'false');
                    toggle.classList.remove('active');
                }
            });
        }
    });
    
    console.log('Accordion menu initialized - only one dropdown can be open at a time');
}

// Global chart variables
let totalContactsChart, totalUsersChart, totalRolesChart, contactStatusGaugeChart, contactFlowChart;

function initCharts() {
    // Initialize ring charts
    createRingChart('totalContactsRing', 1247, 1500, '#3498db');
    createRingChart('totalUsersRing', 25, 50, '#27ae60');
    createRingChart('totalRolesRing', 4, 10, '#9b59b6');
    
    // Initialize contact status gauge
    createContactStatusGauge();
    
    // Initialize contact flow chart with Chart.js
    initializeContactFlowChart();
}

function initializeContactsDashboard() {
    console.log('Initializing Contacts Dashboard...');
    
    // Initialize ring charts with Chart.js
    initializeContactRingCharts();
    
    // Initialize contact status gauge
    createContactStatusGauge();
    
    // Initialize contact flow chart
    initializeContactFlowChart();
    
    // Load initial data
    loadContactData();
    
    // Setup event listeners
    setupContactEventListeners();
}

function initializeContactRingCharts() {
    // Create ring charts using Chart.js for better interactivity
    const totalContactsCtx = document.getElementById('totalContactsRing');
    const totalUsersCtx = document.getElementById('totalUsersRing');
    const totalRolesCtx = document.getElementById('totalRolesRing');
    
    if (totalContactsCtx) {
        totalContactsChart = new Chart(totalContactsCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [1247, 253], // value and remaining
                    backgroundColor: ['#3b82f6', '#f1f5f9'],
                    borderWidth: 0,
                    cutout: '75%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }
    
    if (totalUsersCtx) {
        totalUsersChart = new Chart(totalUsersCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [25, 25], // value and remaining
                    backgroundColor: ['#10b981', '#f1f5f9'],
                    borderWidth: 0,
                    cutout: '75%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }
    
    if (totalRolesCtx) {
        totalRolesChart = new Chart(totalRolesCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [4, 6], // value and remaining
                    backgroundColor: ['#f59e0b', '#f1f5f9'],
                    borderWidth: 0,
                    cutout: '75%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }
}

function initializeContactFlowChart() {
    const canvas = document.getElementById('contactFlowChart');
    if (!canvas) return;
    
    // Sample data for initial chart
    const flowData = {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
        newContacts: [50, 65, 45, 70, 80, 55],
        convertedContacts: [30, 40, 25, 50, 60, 35]
    };
    
    updateContactFlowChart(flowData);
}

function createRingChart(canvasId, value, maxValue, color) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 60;
    const lineWidth = 10;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Background ring
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = lineWidth;
    ctx.stroke();
    
    // Progress ring
    const progress = (value / maxValue) * 2 * Math.PI;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, -Math.PI / 2, -Math.PI / 2 + progress);
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    ctx.stroke();
}

function createContactStatusGauge() {
    const canvas = document.getElementById('contactStatusGauge');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height - 15;
    const radius = 80;
    
    const resolved = 1189;
    const pending = 23;
    const missed = 35;
    const total = resolved + pending + missed;
    
    // Draw gauge background
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI, 0);
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 15;
    ctx.stroke();
    
    // Draw segments
    let currentAngle = Math.PI;
    
    // Resolved (green)
    const resolvedAngle = (resolved / total) * Math.PI;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + resolvedAngle);
    ctx.strokeStyle = '#27ae60';
    ctx.lineWidth = 15;
    ctx.stroke();
    currentAngle += resolvedAngle;
    
    // Pending (orange)
    const pendingAngle = (pending / total) * Math.PI;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + pendingAngle);
    ctx.strokeStyle = '#f39c12';
    ctx.lineWidth = 15;
    ctx.stroke();
    currentAngle += pendingAngle;
    
    // Missed (red)
    const missedAngle = (missed / total) * Math.PI;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + missedAngle);
    ctx.strokeStyle = '#e74c3c';
    ctx.lineWidth = 15;
    ctx.stroke();
    
    // Add labels
    ctx.fillStyle = '#333';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`${Math.round((resolved/total)*100)}% Resolved`, centerX - 50, centerY + 25);
    ctx.fillText(`${Math.round((pending/total)*100)}% Pending`, centerX, centerY + 40);
    ctx.fillText(`${Math.round((missed/total)*100)}% Missed`, centerX + 50, centerY + 25);
}

function createTimelineChart() {
    const canvas = document.getElementById('contactFlowChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Sample data
    const data = [120, 135, 142, 158, 165, 180, 175, 190, 205, 220, 235, 250];
    const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Find min and max values
    const min = Math.min(...data);
    const max = Math.max(...data);
    
    // Draw line chart
    ctx.beginPath();
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 2;
    
    data.forEach((value, index) => {
        const x = (index / (data.length - 1)) * width;
        const y = height - ((value - min) / (max - min)) * height;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
    
    // Add data points
    data.forEach((value, index) => {
        const x = (index / (data.length - 1)) * width;
        const y = height - ((value - min) / (max - min)) * height;
        
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fillStyle = '#667eea';
        ctx.fill();
    });
}

function setupEventListeners() {
    // Modal controls
    const modal = document.getElementById('contactModal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Button event listeners
    document.getElementById('viewUsersBtn').addEventListener('click', () => {
        loadUserData();
    });
    
    document.getElementById('viewContactsBtn').addEventListener('click', () => {
        loadContactData();
    });

    // User Roles Management JavaScript
    const userModal = document.getElementById('userModal');
    const addUserBtn = document.getElementById('addUserBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const userModalCloseBtn = document.querySelector('#userModal .close');

    // Modal controls
    addUserBtn.addEventListener('click', () => {
        currentEditingUser = null;
        document.getElementById('modalTitle').textContent = 'Add New User';
        document.getElementById('userForm').reset();
        document.getElementById('userForm').action = "/api/users"; // Default action for new user
        userModal.style.display = 'block';
    });

    // Close button (×) event listener
    if (userModalCloseBtn) {
        userModalCloseBtn.addEventListener('click', () => {
            userModal.style.display = 'none';
        });
    }

    cancelBtn.addEventListener('click', () => {
        userModal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === userModal) {
            userModal.style.display = 'none';
        }
    });

    // Close modal with ESC key
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && userModal.style.display === 'block') {
            userModal.style.display = 'none';
        }
    });

    // Form submission with AJAX
    document.getElementById('userForm').addEventListener('submit', handleUserSubmit);

    // Filters
    const userSearch = document.getElementById('userSearch');
    const roleFilter = document.getElementById('roleFilter');
    const statusFilter = document.getElementById('statusFilter');

    // Permissions
    const selectedRole = document.getElementById('selectedRole');
    const savePermissionsBtn = document.getElementById('savePermissionsBtn');
    const resetPermissionsBtn = document.getElementById('resetPermissionsBtn');

    // Permissions
    selectedRole.addEventListener('change', renderPermissions);
    savePermissionsBtn.addEventListener('click', savePermissions);
    resetPermissionsBtn.addEventListener('click', resetPermissions);
}

function loadUserData() {
    // Redirect to user management page
    window.location.href = "/userdata";
}

function loadContactData() {
    console.log('Fetching contact data...');
    // Simulate fetching data from an API
    const data = {
        totalContacts: 1247,
        totalUsers: 25,
        totalRoles: 4, // Active Roles
        contactStatus: {
            active: 950,
            inactive: 297
        },
        contactChannels: {
            phone: 810,
            chat: 312,
            email: 87,
            sms: 38
        },
        contactFlow: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
            newContacts: [50, 65, 45, 70, 80, 55],
            convertedContacts: [30, 40, 25, 50, 60, 35]
        },
        userRoles: {
            counselors: 12,
            supervisors: 3,
            administrators: 2,
            volunteers: 8,
            onDuty: 6
        },
        recentContacts: [
            { id: 'C1001', name: 'Alice Smith', type: 'Client', lastContact: '2 days ago', channel: 'Phone' },
            { id: 'C1002', name: 'Bob Johnson', type: 'Partner', lastContact: '1 week ago', channel: 'Email' },
            { id: 'C1003', name: 'Charlie Brown', type: 'Client', lastContact: '5 hours ago', channel: 'Chat' },
            { id: 'U005', name: 'Diana Prince', type: 'Staff', lastContact: 'Logged in now', channel: 'N/A' }
        ]
    };

    updateMetrics(data);
    updateContactChannels(data.contactChannels);
    updateContactFlowChart(data.contactFlow);
    updateUserRoles(data.userRoles);
}

function updateMetrics(data) {
    // Update displayed numbers
    document.getElementById('totalContactsDisplay').textContent = data.totalContacts.toLocaleString();
    document.getElementById('totalUsersDisplay').textContent = data.totalUsers.toLocaleString();
    document.getElementById('totalRolesDisplay').textContent = data.totalRoles.toLocaleString();

    // Update ring charts
    if (totalContactsChart) totalContactsChart.destroy();
    totalContactsChart = createRingChart('totalContactsRing', data.totalContacts, 'Total Contacts', '#3b82f6');

    if (totalUsersChart) totalUsersChart.destroy();
    totalUsersChart = createRingChart('totalUsersRing', data.totalUsers, 'Total Users', '#10b981');

    if (totalRolesChart) totalRolesChart.destroy();
    totalRolesChart = createRingChart('totalRolesRing', data.totalRoles, 'Active Roles', '#f59e0b');

    // Update Contact Status Gauge
    if (contactStatusGaugeChart) contactStatusGaugeChart.destroy();
    contactStatusGaugeChart = createContactStatusGauge('contactStatusGauge', data.contactStatus);
}

function updateContactChannels(channels) {
    const total = Object.values(channels).reduce((sum, count) => sum + count, 0);

    document.querySelector('.phone-progress').style.width = `${(channels.phone / total * 100).toFixed(0)}%`;
    document.querySelector('.chat-progress').style.width = `${(channels.chat / total * 100).toFixed(0)}%`;
    document.querySelector('.email-progress').style.width = `${(channels.email / total * 100).toFixed(0)}%`;
    document.querySelector('.sms-progress').style.width = `${(channels.sms / total * 100).toFixed(0)}%`;

    document.querySelector('.method-bar .method-count').textContent = channels.phone;
    document.querySelector('.method-bar:nth-child(2) .method-count').textContent = channels.chat;
    document.querySelector('.method-bar:nth-child(3) .method-count').textContent = channels.email;
    document.querySelector('.method-bar:nth-child(4) .method-count').textContent = channels.sms;
}

function updateContactFlowChart(flowData) {
    if (contactFlowChart) contactFlowChart.destroy();
    const ctx = document.getElementById('contactFlowChart').getContext('2d');
    contactFlowChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: flowData.labels,
            datasets: [
                {
                    label: 'New Contacts',
                    data: flowData.newContacts,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: '#3b82f6'
                },
                {
                    label: 'Converted to Users',
                    data: flowData.convertedContacts,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: '#10b981'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { usePointStyle: true, padding: 15 }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)'
                }
            },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

function updateUserRoles(roles) {
    document.getElementById('counselorCount').textContent = roles.counselors;
    document.getElementById('supervisorCount').textContent = roles.supervisors;
    document.getElementById('adminCount').textContent = roles.administrators;
    document.getElementById('volunteerCount').textContent = roles.volunteers;
    document.getElementById('onDutyCount').textContent = roles.onDuty;
    document.getElementById('totalUsers').textContent = roles.counselors + roles.supervisors + roles.administrators + roles.volunteers; // Sum for total users
}

function setupContactEventListeners() {
    const modal = document.getElementById('contactModal');
    const closeBtn = document.querySelector('.modal .close');
    const viewUsersBtn = document.getElementById('viewUsersBtn');
    const viewContactsBtn = document.getElementById('viewContactsBtn');

    if (closeBtn) {
        closeBtn.onclick = function() {
            modal.classList.remove('show');
        }
    }

    if (viewUsersBtn) {
        viewUsersBtn.onclick = function() {
            showContactModal('users');
        }
    }

    if (viewContactsBtn) {
        viewContactsBtn.onclick = function() {
            showContactModal('contacts');
        }
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.classList.remove('show');
        }
    }
}

function showContactModal(dataType) {
    const modal = document.getElementById('contactModal');
    const modalContentDiv = document.getElementById('modalContent');

    modalContentDiv.innerHTML = '<div class="loading-spinner">Loading...</div>'; // Simple loading indicator
    modal.classList.add('show'); // Use class instead of direct style

    // Simulate API call for modal content
    setTimeout(() => {
        let contentHtml = '';
        if (dataType === 'users') {
            contentHtml = `
                <h2>All Users</h2>
                <p>Detailed list of all registered users in the system.</p>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr><th>User ID</th><th>Name</th><th>Role</th><th>Status</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>U001</td><td>Marlon</td><td>Counselor</td><td>Active</td></tr>
                            <tr><td>U002</td><td>Jane Doe</td><td>Supervisor</td><td>Active</td></tr>
                            <tr><td>U003</td><td>John Smith</td><td>Counselor</td><td>Offline</td></tr>
                            <tr><td>U004</td><td>Admin A</td><td>Administrator</td><td>Active</td></tr>
                            <tr><td>U005</td><td>Volunteer B</td><td>Volunteer</td><td>Active</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
        } else if (dataType === 'contacts') {
            contentHtml = `
                <h2>All Contacts</h2>
                <p>Comprehensive list of all helpline contacts.</p>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr><th>Contact ID</th><th>Name/Identifier</th><th>Last Contact</th><th>Channel</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>C1001</td><td>Alice Smith</td><td>2024-06-11</td><td>Phone</td></tr>
                            <tr><td>C1002</td><td>Bob Johnson</td><td>2024-06-07</td><td>Email</td></tr>
                            <tr><td>C1003</td><td>Charlie Brown</td><td>2024-06-13</td><td>Chat</td></tr>
                            <tr><td>C1004</td><td>Anonymous Caller</td><td>2024-06-13</td><td>Phone</td></tr>
                            <tr><td>C1005</td><td>Project X Member</td><td>2024-06-10</td><td>SMS</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
        }
        modalContentDiv.innerHTML = contentHtml;
    }, 500); // Simulate network delay
}

function initializeCallCharts() {
    console.log('Creating Call Data charts...');
    
    // Call Volume Chart
    const volumeCtx = document.getElementById('callVolumeChart');
    if (volumeCtx) {
        new Chart(volumeCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
                datasets: [{
                    label: 'Inbound Calls',
                    data: [12, 8, 15, 45, 65, 85, 75, 35],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 3,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#3b82f6'
                }, {
                    label: 'Outbound Calls',
                    data: [5, 3, 8, 25, 35, 45, 30, 15],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 3,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#10b981'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: '#3b82f6',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }

    // Call Distribution Chart
    const distributionCtx = document.getElementById('callDistributionChart');
    if (distributionCtx) {
        new Chart(distributionCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Emergency', 'General Inquiry', 'Support', 'Follow-up', 'Other'],
                datasets: [{
                    data: [15, 35, 25, 15, 10],
                    backgroundColor: [
                        '#ef4444',
                        '#f59e0b',
                        '#10b981',
                        '#3b82f6',
                        '#8b5cf6'
                    ],
                    borderColor: [
                        '#dc2626',
                        '#d97706',
                        '#059669',
                        '#2563eb',
                        '#7c3aed'
                    ],
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 15,
                            font: {
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }

    // Agent Performance Chart
    const performanceCtx = document.getElementById('agentPerformanceChart');
    if (performanceCtx) {
        new Chart(performanceCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['John D.', 'Sarah M.', 'Mike R.', 'Lisa K.', 'Tom B.'],
                datasets: [{
                    label: 'Calls Handled',
                    data: [45, 38, 42, 35, 40],
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(139, 92, 246, 0.8)'
                    ],
                    borderColor: [
                        '#3b82f6',
                        '#10b981',
                        '#f59e0b',
                        '#ef4444',
                        '#8b5cf6'
                    ],
                    borderWidth: 2,
                    borderRadius: 6,
                    maxBarThickness: 35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        callbacks: {
                            label: function(context) {
                                return `Calls Handled: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 10
                            }
                        }
                    }
                }
            }
        });
    }
}

function loadCallData() {
    console.log('Loading call data...');
    // Simulate fetching data for quick stats and recent calls
    const dummyCallData = {
        totalCallsToday: 187,
        activeCalls: 7,
        avgCallDuration: '8m 30s',
        peakHours: '10:00 - 12:00',
        activeAgents: 22,
        callsPerAgent: '8.5',
        firstCallResolution: '78%',
        satisfactionRate: '92%',
        recentCalls: [
            { id: 'C98765', time: '14:30', agent: 'Alice B.', type: 'Inbound', category: 'Support', duration: '05:10', status: 'Completed', resolution: 'Resolved', satisfaction: 'High' },
            { id: 'C98764', time: '14:25', agent: 'Bob C.', type: 'Outbound', category: 'Follow-up', duration: '03:45', status: 'Completed', resolution: 'Resolved', satisfaction: 'Medium' },
            { id: 'C98763', time: '14:15', agent: 'Alice B.', type: 'Emergency', category: 'Crisis', duration: '12:30', status: 'In Progress', resolution: 'Ongoing', satisfaction: 'N/A' },
            { id: 'C98762', time: '14:00', agent: 'Charlie D.', type: 'Inbound', category: 'General Inquiry', duration: '02:15', status: 'Completed', resolution: 'Resolved', satisfaction: 'High' },
            { id: 'C98761', time: '13:55', agent: 'Bob C.', type: 'Callback', category: 'Support', duration: '07:20', status: 'Completed', resolution: 'Resolved', satisfaction: 'High' },
            { id: 'C98760', time: '13:40', agent: 'Alice B.', type: 'Inbound', category: 'Technical', duration: '09:00', status: 'In Progress', resolution: 'Ongoing', satisfaction: 'N/A' },
            { id: 'C98759', time: '13:30', agent: 'Charlie D.', type: 'Emergency', category: 'Safety', duration: '06:50', status: 'Completed', resolution: 'Resolved', satisfaction: 'N/A' },
            { id: 'C98758', time: '13:20', agent: 'Alice B.', type: 'Inbound', category: 'Billing', duration: '04:00', status: 'Completed', resolution: 'Resolved', satisfaction: 'Low' },
            { id: 'C98757', time: '13:10', agent: 'Bob C.', type: 'Outbound', category: 'Feedback', duration: '02:50', status: 'Completed', resolution: 'Resolved', satisfaction: 'High' },
            { id: 'C98756', time: '13:00', agent: 'Charlie D.', type: 'Inbound', category: 'Product', duration: '03:10', status: 'Completed', resolution: 'Resolved', satisfaction: 'Medium' },
        ],
        queueStatus: [
            { id: 'Q001', type: 'Emergency', waitTime: '1 min', callsInQueue: 1 },
            { id: 'Q002', type: 'General Inquiry', waitTime: '3 min', callsInQueue: 3 },
            { id: 'Q003', type: 'Support', waitTime: '2 min', callsInQueue: 2 }
        ]
    };

    // Update quick stats
    document.getElementById('totalCallsToday').textContent = dummyCallData.totalCallsToday;
    document.getElementById('activeCalls').textContent = dummyCallData.activeCalls;
    document.getElementById('avgCallDuration').textContent = dummyCallData.avgCallDuration;
    document.getElementById('peakHours').textContent = dummyCallData.peakHours;
    document.getElementById('activeAgents').textContent = dummyCallData.activeAgents;
    document.getElementById('callsPerAgent').textContent = dummyCallData.callsPerAgent;
    document.getElementById('firstCallResolution').textContent = dummyCallData.firstCallResolution;
    document.getElementById('satisfactionRate').textContent = dummyCallData.satisfactionRate;

    // Update recent calls table
    renderRecentCallsTable(dummyCallData.recentCalls);

    // Update queue status
    renderQueueStatus(dummyCallData.queueStatus);
}

function setupCallEventListeners() {
    // Search input
    const callSearchInput = document.getElementById('callSearch');
    if (callSearchInput) {
        callSearchInput.addEventListener('input', debounce(filterCalls, 300));
    }

    // Filter selects
    document.getElementById('callTypeFilter')?.addEventListener('change', filterCalls);
    document.getElementById('statusFilter')?.addEventListener('change', filterCalls);
    document.getElementById('timeFilter')?.addEventListener('change', filterCalls);
    document.getElementById('distributionType')?.addEventListener('change', updateDistributionChart);
    document.getElementById('performanceMetric')?.addEventListener('change', updatePerformanceChart);

    // Chart view buttons for Call Volume Trends
    document.querySelectorAll('#callVolumeChart + .chart-actions .btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('#callVolumeChart + .chart-actions .btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateVolumeChart(this.dataset.view);
        });
    });
}

function startRealTimeCallUpdates() {
    // This is where you would implement WebSocket or polling for real-time data
    setInterval(updateCallDashboard, 30000); // Update every 30 seconds
}

// Utility function to debounce for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Rendering functions for specific sections
function renderRecentCallsTable(calls) {
    const tableBody = document.querySelector('#callsTable tbody');
    if (!tableBody) return;

    tableBody.innerHTML = calls.map(call => `
        <tr>
            <td>${call.id}</td>
            <td>${call.time}</td>
            <td>${call.agent}</td>
            <td>${call.type}</td>
            <td>${call.category}</td>
            <td>${call.duration}</td>
            <td><span class="badge bg-${getCallStatusClass(call.status)}">${call.status}</span></td>
            <td>${call.resolution}</td>
            <td><span class="badge bg-${getSatisfactionClass(call.satisfaction)}">${call.satisfaction}</span></td>
            <td>
                <button class="btn btn-sm btn-outline-secondary" onclick="viewCallDetails('${call.id}')">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        </tr>
    `).join('');

    // Update table info (assuming pagination is handled elsewhere or is simple)
    const tableStart = document.getElementById('tableStart');
    const tableEnd = document.getElementById('tableEnd');
    const tableTotal = document.getElementById('tableTotal');
    if (tableStart && tableEnd && tableTotal) {
        tableStart.textContent = calls.length > 0 ? 1 : 0;
        tableEnd.textContent = calls.length;
        tableTotal.textContent = calls.length; // For this simple example, total equals displayed
    }
}

function renderQueueStatus(queueItems) {
    const queueList = document.getElementById('queueStatus');
    if (!queueList) return;

    queueList.innerHTML = queueItems.map(item => `
        <div class="queue-item">
            <div class="queue-item-info">
                <div class="queue-item-label">${item.type} Queue</div>
                <div class="queue-item-value">${item.callsInQueue} calls, est. ${item.waitTime} wait</div>
            </div>
            <button class="btn btn-sm btn-outline-primary">View</button>
        </div>
    `).join('');
}


// Utility functions for badge classes
function getCallStatusClass(status) {
    switch(status.toLowerCase()) {
        case 'completed': return 'success';
        case 'in progress': return 'warning';
        case 'missed': return 'danger';
        case 'scheduled': return 'info';
        default: return 'secondary';
    }
}

function getSatisfactionClass(satisfaction) {
    switch(satisfaction.toLowerCase()) {
        case 'high': return 'success';
        case 'medium': return 'warning';
        case 'low': return 'danger';
        default: return 'secondary';
    }
}

// Dummy functions for events (replace with actual logic)
function filterCalls() {
    console.log('Filtering calls based on search and filters...');
    // Implement filtering logic here
}

function updateDistributionChart() {
    console.log('Updating call distribution chart based on selection...');
    // Update chart data/labels based on distributionType select value
}

function updatePerformanceChart() {
    console.log('Updating agent performance chart based on selection...');
    // Update chart data/labels based on performanceMetric select value
}

function updateVolumeChart(view) {
    console.log('Updating call volume chart view:', view);
    // Adjust data for callVolumeChart based on 'daily', 'weekly', 'monthly' views
}

function refreshQueue() {
    console.log('Refreshing queue status...');
    // Fetch latest queue data and re-renderQueueStatus
    loadCallData(); // For this example, reloads all data
}

function refreshTable() {
    console.log('Refreshing recent calls table...');
    // Fetch latest call data and re-renderRecentCallsTable
    loadCallData(); // For this example, reloads all data
}

function toggleColumns() {
    console.log('Toggling column visibility...');
    alert('Column toggle feature coming soon!');
    // Implement logic to show/hide columns in #callsTable
}

function openNewCallForm() {
    console.log('Opening new call form...');
    alert('New Call form feature coming soon!');
    // Implement modal or page navigation for new call form
}

function exportCallData() {
    console.log('Exporting call data...');
    alert('Call data export feature coming soon!');
    // Implement data export logic (e.g., CSV, Excel)
}

function updateCallDashboard() {
    console.log('Updating Call Data Dashboard in real-time...');
    // Fetch and update relevant metrics and lists without full reload
    loadCallData();
}

function viewCallDetails(callId) {
    console.log('Viewing details for call:', callId);
    alert(`Viewing details for Call ID: ${callId}`);
    // Implement showing a modal or navigating to a detail page for the call
}

function initializeCaseCharts() {
    console.log('Creating Case Management charts...');

    // Case Trends Chart
    const trendsCtx = document.getElementById('caseTrendsChart');
    if (trendsCtx) {
        new Chart(trendsCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'New Cases',
                    data: [65, 59, 80, 81, 56, 55],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 3,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#3b82f6'
                }, {
                    label: 'Resolved Cases',
                    data: [28, 48, 40, 19, 86, 27],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 3,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#10b981'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: '#3b82f6',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }

    // Case Distribution Chart
    const distributionCtx = document.getElementById('caseDistributionChart');
    if (distributionCtx) {
        new Chart(distributionCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Child Protection', 'GBV', 'Mental Health', 'Family', 'Other'],
                datasets: [{
                    data: [30, 25, 20, 15, 10],
                    backgroundColor: [
                        '#ef4444',
                        '#f59e0b',
                        '#10b981',
                        '#3b82f6',
                        '#8b5cf6'
                    ],
                    borderColor: [
                        '#dc2626',
                        '#d97706',
                        '#059669',
                        '#2563eb',
                        '#7c3aed'
                    ],
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 15,
                            font: {
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }

    // Staff Performance Chart
    const performanceCtx = document.getElementById('staffPerformanceChart');
    if (performanceCtx) {
        new Chart(performanceCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['John D.', 'Sarah M.', 'Mike R.', 'Lisa K.', 'Tom B.'],
                datasets: [{
                    label: 'Cases Handled',
                    data: [45, 38, 42, 35, 40],
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(139, 92, 246, 0.8)'
                    ],
                    borderColor: [
                        '#3b82f6',
                        '#10b981',
                        '#f59e0b',
                        '#ef4444',
                        '#8b5cf6'
                    ],
                    borderWidth: 2,
                    borderRadius: 6,
                    maxBarThickness: 35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        callbacks: {
                            label: function(context) {
                                return `Cases Handled: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 10
                            }
                        }
                    }
                }
            }
        });
    }
}

function loadCaseData() {
    console.log('Loading case data...');
    // Simulate fetching data for quick stats, recent activity, and cases table
    const dummyCaseData = {
        totalActiveCases: 156,
        newCasesToday: 12,
        urgentCases: 23,
        avgResponseTime: '0.8h',
        resolutionRate: '85%',
        avgResolutionTime: '3.5d',
        activeStaff: 28,
        casesPerStaff: '5.6',
        recentActivity: [
            { type: 'case', title: 'New Case: Mental Health Support', description: 'Client reported anxiety symptoms. Assigned to Sarah M.', time: '5 minutes ago' },
            { type: 'case', title: 'Case Updated: Child Protection', description: 'Follow-up visit scheduled for Case #20240032', time: '30 minutes ago' },
            { type: 'staff', title: 'Staff Login: John D.', description: 'John D. logged in and is now available.', time: '1 hour ago' },
            { type: 'case', title: 'Case Resolved: Domestic Violence', description: 'Case #20240028 closed, client referred to shelter.', time: '2 hours ago' },
            { type: 'system', title: 'Data Sync Complete', description: 'Case data synchronized with external database.', time: '3 hours ago' },
        ],
        allCases: [
            { id: '20240035', title: 'Mental Health Support', client: 'Jane D.', category: 'Mental Health', priority: 'High', status: 'New', assignedTo: 'Sarah M.', created: '2024-06-13 14:00', lastUpdated: '2024-06-13 14:05' },
            { id: '20240034', title: 'Family Dispute Mediation', client: 'The Smiths', category: 'Family', priority: 'Medium', status: 'In Progress', assignedTo: 'John D.', created: '2024-06-12 10:30', lastUpdated: '2024-06-13 09:15' },
            { id: '20240033', title: 'Child Protection Referral', client: 'Anon.', category: 'Child Protection', priority: 'Urgent', status: 'Open', assignedTo: 'Lisa K.', created: '2024-06-11 16:45', lastUpdated: '2024-06-13 11:20' },
            { id: '20240032', title: 'GBV Support', client: 'Emily R.', category: 'GBV', priority: 'High', status: 'Pending', assignedTo: 'Mike R.', created: '2024-06-10 09:00', lastUpdated: '2024-06-13 13:00' },
            { id: '20240031', title: 'Housing Assistance', client: 'David L.', category: 'Social Support', priority: 'Low', status: 'Resolved', assignedTo: 'Tom B.', created: '2024-06-09 11:10', lastUpdated: '2024-06-12 17:00' },
            { id: '20240030', title: 'Elder Abuse Report', client: 'Anon.', category: 'Elderly Care', priority: 'Urgent', status: 'Open', assignedTo: 'Sarah M.', created: '2024-06-08 15:00', lastUpdated: '2024-06-13 10:00' },
            { id: '20240029', title: 'Legal Aid Query', client: 'Robert F.', category: 'Legal', priority: 'Medium', status: 'Closed', assignedTo: 'John D.', created: '2024-06-07 13:00', lastUpdated: '2024-06-10 14:30' },
            { id: '20240028', title: 'Substance Abuse Support', client: 'Chris G.', category: 'Mental Health', priority: 'High', status: 'In Progress', assignedTo: 'Lisa K.', created: '2024-06-06 09:30', lastUpdated: '2024-06-13 08:00' },
            { id: '20240027', title: 'Disability Support', client: 'Maria P.', category: 'Social Support', priority: 'Low', status: 'Resolved', assignedTo: 'Mike R.', created: '2024-06-05 10:00', lastUpdated: '2024-06-11 16:00' },
            { id: '20240026', title: 'Education Guidance', client: 'Alex H.', category: 'Youth', priority: 'Low', status: 'Closed', assignedTo: 'Tom B.', created: '2024-06-04 14:00', lastUpdated: '2024-06-07 11:00' },
        ]
    };

    // Update quick stats
    document.getElementById('totalActiveCases').textContent = dummyCaseData.totalActiveCases;
    document.getElementById('newCasesToday').textContent = dummyCaseData.newCasesToday;
    document.getElementById('urgentCases').textContent = dummyCaseData.urgentCases;
    document.getElementById('avgResponseTime').textContent = dummyCaseData.avgResponseTime;
    document.getElementById('resolutionRate').textContent = dummyCaseData.resolutionRate;
    document.getElementById('avgResolutionTime').textContent = dummyCaseData.avgResolutionTime;
    document.getElementById('activeStaff').textContent = dummyCaseData.activeStaff;
    document.getElementById('casesPerStaff').textContent = dummyCaseData.casesPerStaff;

    // Update recent activity
    renderRecentActivity(dummyCaseData.recentActivity);

    // Update cases table
    renderCasesTable(dummyCaseData.allCases);
}

function setupCaseEventListeners() {
    // Search input
    const caseSearchInput = document.getElementById('caseSearch');
    if (caseSearchInput) {
        caseSearchInput.addEventListener('input', debounce(filterCases, 300));
    }

    // Filter selects
    document.getElementById('statusFilter')?.addEventListener('change', filterCases);
    document.getElementById('priorityFilter')?.addEventListener('change', filterCases);
    document.getElementById('timeFilter')?.addEventListener('change', filterCases);
    document.getElementById('distributionType')?.addEventListener('change', updateCaseDistributionChart);
    document.getElementById('performanceMetric')?.addEventListener('change', updateStaffPerformanceChart);

    // Chart view buttons for Case Trends Chart
    document.querySelectorAll('#caseTrendsChart + .chart-actions .btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('#caseTrendsChart + .chart-actions .btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateCaseTrendsChart(this.dataset.view);
        });
    });
}

function startRealTimeCaseUpdates() {
    // Implement real-time updates using WebSocket or polling
    setInterval(updateCaseDashboard, 30000); // Update every 30 seconds
}

// Rendering functions for specific sections
function renderRecentActivity(activities) {
    const activityList = document.getElementById('recentActivity');
    if (!activityList) return;

    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-icon ${activity.type}">${getActivityIcon(activity.type)}</div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-description">${activity.description}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
        </div>
    `).join('');
}

function renderCasesTable(cases) {
    const tableBody = document.querySelector('#casesTable tbody');
    if (!tableBody) return;

    tableBody.innerHTML = cases.map(caseItem => `
        <tr>
            <td>${caseItem.id}</td>
            <td>${caseItem.title}</td>
            <td>${caseItem.client}</td>
            <td>${caseItem.category}</td>
            <td><span class="badge bg-${getPriorityClass(caseItem.priority)}">${caseItem.priority}</span></td>
            <td><span class="badge bg-${getCaseStatusClass(caseItem.status)}">${caseItem.status}</span></td>
            <td>${caseItem.assignedTo}</td>
            <td>${caseItem.created}</td>
            <td>${caseItem.lastUpdated}</td>
            <td>
                <button class="btn btn-sm btn-outline-secondary" onclick="viewCaseDetails('${caseItem.id}')">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        </tr>
    `).join('');

    // Update table info (assuming pagination is handled elsewhere or is simple)
    const tableStart = document.getElementById('tableStart');
    const tableEnd = document.getElementById('tableEnd');
    const tableTotal = document.getElementById('tableTotal');
    if (tableStart && tableEnd && tableTotal) {
        tableStart.textContent = cases.length > 0 ? 1 : 0;
        tableEnd.textContent = cases.length;
        tableTotal.textContent = cases.length; // For this simple example, total equals displayed
    }
}


// Utility functions for badge classes and icons
function getActivityIcon(type) {
    const icons = {
        'call': '📞',
        'case': '📁',
        'staff': '👥',
        'system': '⚙️'
    };
    return icons[type] || '📌';
}

function getPriorityClass(priority) {
    switch(priority.toLowerCase()) {
        case 'urgent': return 'danger';
        case 'high': return 'warning';
        case 'medium': return 'info';
        case 'low': return 'success';
        default: return 'secondary';
    }
}

function getCaseStatusClass(status) {
    switch(status.toLowerCase()) {
        case 'new': return 'primary';
        case 'open': return 'danger';
        case 'in-progress': return 'warning';
        case 'pending': return 'info';
        case 'resolved': return 'success';
        case 'closed': return 'secondary';
        default: return 'secondary';
    }
}

// Dummy functions for events (replace with actual logic)
function filterCases() {
    console.log('Filtering cases based on search and filters...');
    // Implement filtering logic here
}

function updateCaseDistributionChart() {
    console.log('Updating case distribution chart based on selection...');
    // Update chart data/labels based on distributionType select value
}

function updateStaffPerformanceChart() {
    console.log('Updating staff performance chart based on selection...');
    // Update chart data/labels based on performanceMetric select value
}

function updateCaseTrendsChart(view) {
    console.log('Updating case trends chart view:', view);
    // Adjust data for caseTrendsChart based on 'volume', 'resolution', 'response' views
}

function refreshActivity() {
    console.log('Refreshing recent activity...');
    // Fetch latest activity data and re-renderRecentActivity
    loadCaseData(); // For this example, reloads all data
}

function refreshTable() {
    console.log('Refreshing all cases table...');
    // Fetch latest case data and re-renderCasesTable
    loadCaseData(); // For this example, reloads all data
}

function toggleColumns() {
    console.log('Toggling column visibility...');
    alert('Column toggle feature coming soon!');
    // Implement logic to show/hide columns in #casesTable
}

function openNewCaseForm() {
    console.log('Opening new case form...');
    alert('New Case form feature coming soon!');
    // Implement modal or page navigation for new case form
}

function exportCaseData() {
    console.log('Exporting case data...');
    alert('Case data export feature coming soon!');
    // Implement data export logic (e.g., CSV, Excel)
}

function updateCaseDashboard() {
    console.log('Updating Case Management Dashboard in real-time...');
    // Fetch and update relevant metrics and lists without full reload
    loadCaseData();
}

function viewCaseDetails(caseId) {
    console.log('Viewing details for case:', caseId);
    alert(`Viewing details for Case ID: ${caseId}`);
    // Implement showing a modal or navigating to a detail page for the case
}

// User Roles Management JavaScript
// Sample data for permissions (in real app, this would come from backend)
const rolePermissions = {
    admin: {
        "User Management": ["Create Users", "Edit Users", "Delete Users", "Assign Roles"],
        "Contact Management": ["View All Contacts", "Edit Contacts", "Delete Contacts", "Export Data"],
        "System Settings": ["Manage Settings", "View Reports", "Backup Data", "System Logs"],
        "Communication": ["Send Messages", "Broadcast Alerts", "Manage Templates"]
    },
    supervisor: {
        "User Management": ["View Users", "Edit Users"],
        "Contact Management": ["View All Contacts", "Edit Contacts", "Export Data"],
        "System Settings": ["View Reports"],
        "Communication": ["Send Messages", "Manage Templates"]
    },
    counselor: {
        "User Management": ["View Users"],
        "Contact Management": ["View Assigned Contacts", "Edit Contacts"],
        "System Settings": [],
        "Communication": ["Send Messages"]
    },
    volunteer: {
        "User Management": [],
        "Contact Management": ["View Assigned Contacts"],
        "System Settings": [],
        "Communication": ["Send Messages"]
    }
};

let currentEditingUser = null;

function renderPermissions() {
    const selectedRole = document.getElementById('selectedRole').value;
    const permissions = rolePermissions[selectedRole];
    const permissionsGrid = document.getElementById('permissionsGrid');

    permissionsGrid.innerHTML = '';

    Object.keys(permissions).forEach(category => {
        const permissionGroup = document.createElement('div');
        permissionGroup.className = 'permission-group';

        let permissionItems = '';
        // For demonstration, we'll check against the current role's permissions
        // In a real app, you'd have a master list of all possible permissions
        // and check if the current role has each one.
        const allPossiblePermissionsForCategory = [
            // This needs to be comprehensive based on your actual permissions
            ...(category === "User Management" ? ["Create Users", "Edit Users", "Delete Users", "Assign Roles", "View Users"] : []),
            ...(category === "Contact Management" ? ["View All Contacts", "Edit Contacts", "Delete Contacts", "Export Data", "View Assigned Contacts"] : []),
            ...(category === "System Settings" ? ["Manage Settings", "View Reports", "Backup Data", "System Logs"] : []),
            ...(category === "Communication" ? ["Send Messages", "Broadcast Alerts", "Manage Templates"] : []),
        ].filter((value, index, self) => self.indexOf(value) === index); // Deduplicate

        allPossiblePermissionsForCategory.forEach(permission => {
            const checked = permissions[category].includes(permission) ? 'checked' : '';
            permissionItems += `
                <div class="permission-item">
                    <input type="checkbox" class="permission-checkbox" ${checked}
                            data-category="${category}" data-permission="${permission}">
                    <label class="permission-label">${permission}</label>
                </div>
            `;
        });

        permissionGroup.innerHTML = `
            <h4>${category}</h4>
            ${permissionItems}
        `;

        permissionsGrid.appendChild(permissionGroup);
    });
}

function filterUsers() {
    const searchTerm = document.getElementById('userSearch').value.toLowerCase();
    const roleFilter = document.getElementById('roleFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;

    const userItems = document.querySelectorAll('.user-item[data-user-id]');

    userItems.forEach(item => {
        const userName = item.querySelector('.user-details h4').textContent.toLowerCase();
        const userEmail = item.querySelector('.user-details p').textContent.toLowerCase();
        const userRoleElement = item.querySelector('.role-badge');
        const userRole = userRoleElement ? userRoleElement.textContent.toLowerCase() : '';
        const userStatusElement = item.querySelector('.status-indicator');
        const userStatus = userStatusElement ? (userStatusElement.className.includes('online') ? 'online' :
                               userStatusElement.className.includes('busy') ? 'busy' : 'offline') : '';

        const matchesSearch = userName.includes(searchTerm) || userEmail.includes(searchTerm);
        const matchesRole = !roleFilter || userRole.includes(roleFilter);
        const matchesStatus = !statusFilter || userStatus === statusFilter;

        if (matchesSearch && matchesRole && matchesStatus) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}

function editUser(userId) {
    // In a real app, fetch user data from backend using the userId
    // For this example, we'll simulate fetching data
    const userItem = document.querySelector(`[data-user-id="${userId}"]`);
    if (!userItem) {
        console.error('User item not found for ID:', userId);
        alert('User not found.');
        return;
    }

    const userName = userItem.querySelector('.user-details h4').textContent;
    const userEmail = userItem.querySelector('.user-details p').textContent.trim().split(/\s+/).pop(); // Get email after status
    const userRole = userItem.querySelector('.role-badge').textContent.toLowerCase().replace(' ', ''); // e.g., "administrator" -> "admin"

    currentEditingUser = userId;
    document.getElementById('modalTitle').textContent = 'Edit User';
    document.getElementById('userName').value = userName;
    document.getElementById('userEmail').value = userEmail;
    document.getElementById('userRole').value = userRole;
    document.getElementById('userPhone').value = ''; // Phone not in sample HTML, would come from real data
    document.getElementById('userForm').action = `/users/${userId}/update/`; // Action for updating user
    document.getElementById('userModal').style.display = 'block';

    // Example of fetching user data from a mock API
    /*
    fetch(`/api/users/${userId}`)
        .then(response => response.json())
        .then(data => {
            currentEditingUser = userId;
            document.getElementById('modalTitle').textContent = 'Edit User';
            document.getElementById('userName').value = data.full_name;
            document.getElementById('userEmail').value = data.email;
            document.getElementById('userRole').value = data.role;
            document.getElementById('userPhone').value = data.phone || '';
            document.getElementById('userForm').action = `/api/users/${userId}`; // Or PUT /api/users/userId
            document.getElementById('userModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading user data:', error);
            alert('Error loading user data. Please try again.');
        });
    */
}

function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        // In a real app, send a DELETE request to your backend
        fetch(`/users/${userId}/delete/`, { // Example endpoint
            method: 'POST', // Or 'DELETE' if your backend supports it directly
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // For Flask/Django XHR detection
                'Content-Type': 'application/json' // If sending JSON body
            },
            // body: JSON.stringify({ user_id: userId }) // If sending JSON body
        })
        .then(response => {
            if (!response.ok) {
                // Check if response is JSON or plain text
                return response.text().then(text => { throw new Error(text || response.statusText); });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Remove user item from DOM
                const userItemToRemove = document.querySelector(`[data-user-id="${userId}"]`);
                if (userItemToRemove) {
                    userItemToRemove.remove();
                }
                updateRoleCounts();
                alert('User deleted successfully');
            } else {
                alert('Error deleting user: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            alert('Error deleting user. Please try again. Details: ' + error.message);
        });
    }
}

function handleUserSubmit(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const userId = currentEditingUser;
    let url = e.target.action;
    let method = 'POST';

    // If editing, you might use a PUT method and a different URL structure
    // For this example, we'll stick to POST, as the Flask route indicates
    // `/users/{userId}/update/` for POST.
    // If your backend expects a PUT for updates, you'd adjust method and URL.
    /*
    if (userId) { // If editing an existing user
        method = 'PUT';
        url = `/api/users/${userId}`;
    }
    */

    fetch(url, {
        method: method,
        body: formData, // Use formData directly for multipart/form-data
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
            // 'Content-Type': 'application/json' is NOT set when using FormData directly,
            // as the browser handles it (multipart/form-data)
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text || response.statusText); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            document.getElementById('userModal').style.display = 'none';
            // In a real application, you might update the specific user item
            // or re-fetch a small portion of the user list.
            // For simplicity, a full page reload often suffices during development.
            location.reload();
        } else {
            alert('Error saving user: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error saving user:', error);
        alert('Error saving user. Please try again. Details: ' + error.message);
    });
}

function updateRoleCounts() {
    // This function calculates counts from the DOM.
    // In a production app, these counts would ideally come from your backend.
    const userItems = document.querySelectorAll('.user-item[data-user-id]');
    const counts = { admin: 0, supervisor: 0, counselor: 0, volunteer: 0, online: 0, busy: 0, offline: 0 };

    userItems.forEach(item => {
        const roleBadge = item.querySelector('.role-badge');
        if (roleBadge) {
            const roleText = roleBadge.textContent.toLowerCase();
            if (roleText.includes('admin')) counts.admin++;
            if (roleText.includes('supervisor')) counts.supervisor++;
            if (roleText.includes('counselor')) counts.counselor++;
            if (roleText.includes('volunteer')) counts.volunteer++;
        }

        const statusIndicator = item.querySelector('.status-indicator');
        if (statusIndicator) {
            if (statusIndicator.className.includes('status-online')) counts.online++;
            else if (statusIndicator.className.includes('status-busy')) counts.busy++;
            else if (statusIndicator.className.includes('status-offline')) counts.offline++;
        }
    });

    document.getElementById('adminCount').textContent = counts.admin;
    document.getElementById('supervisorCount').textContent = counts.supervisor;
    document.getElementById('counselorCount').textContent = counts.counselor;
    document.getElementById('volunteerCount').textContent = counts.volunteer;
    document.getElementById('onlineCount').textContent = counts.online;
    // Potentially add busy/offline counts to UI if desired
}

function savePermissions() {
    const selectedRole = document.getElementById('selectedRole').value;
    const checkboxes = document.querySelectorAll('.permission-checkbox');

    const permissionsToSave = {};
    checkboxes.forEach(checkbox => {
        const category = checkbox.dataset.category;
        const permission = checkbox.dataset.permission;

        if (!permissionsToSave[category]) {
            permissionsToSave[category] = [];
        }

        if (checkbox.checked) {
            permissionsToSave[category].push(permission);
        }
    });

    // In a real app, send this `permissionsToSave` data to your backend
    fetch('/users/permissions/save/', { // Example endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            role: selectedRole,
            permissions: permissionsToSave
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text || response.statusText); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update the local `rolePermissions` object to reflect changes
            rolePermissions[selectedRole] = permissionsToSave;
            alert('Permissions saved successfully!');
        } else {
            alert('Error saving permissions: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error saving permissions:', error);
        alert('Error saving permissions. Please try again. Details: ' + error.message);
    });
}

function resetPermissions() {
    if (confirm('Are you sure you want to reset permissions to default? This will not save to the backend unless you click "Save Changes".')) {
        // This simulates resetting to the initial sample data.
        // In a real application, you might fetch default permissions from the server.
        // For simplicity, we'll re-render based on the initial `rolePermissions` object.
        renderPermissions();
        alert('Permissions display reset to default values. Click "Save Changes" to apply this permanently.');
    }
}

// Theme Toggle Function
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    // Update theme attribute on body
    body.setAttribute('data-theme', newTheme);
    
    // Store theme preference
    localStorage.setItem('theme', newTheme);
    
    // Update theme button text
    const themeBtn = document.querySelector('.theme-btn span');
    if (themeBtn) {
        themeBtn.textContent = newTheme === 'dark' ? 'Light Theme' : 'Dark Theme';
    }
    
    // Update theme icon
    const themeIcon = document.querySelector('.theme-btn .nav-icon');
    if (themeIcon) {
        themeIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
    }
    
    // Apply theme changes globally
    applyTheme(newTheme);
}

// Apply Theme Function - Global Application
function applyTheme(theme) {
    // Apply to all sidebar elements
    const sidebars = document.querySelectorAll('.sidebar');
    const mainContents = document.querySelectorAll('.main-content');
    
    sidebars.forEach(sidebar => {
        if (theme === 'light') {
            sidebar.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
        } else {
            sidebar.style.background = 'linear-gradient(135deg, #2d1b14 0%, #5d4037 100%)';
        }
    });
    
    mainContents.forEach(mainContent => {
        if (theme === 'light') {
            mainContent.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
        } else {
            mainContent.style.background = 'linear-gradient(135deg, #2d1b14 0%, #5d4037 100%)';
        }
    });
    
    // Apply theme to all dashboard elements
    applyThemeToElements(theme);
}

// Apply theme to all dashboard elements
function applyThemeToElements(theme) {
    // Apply to all cards, headers, buttons, etc.
    const elements = {
        '.dashboard-header': theme === 'light' ? 
            'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)' : 
            'linear-gradient(135deg, rgba(45, 27, 20, 0.9) 0%, rgba(93, 64, 55, 0.8) 100%)',
        '.stat-card': theme === 'light' ? 
            'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)' : 
            'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(245, 245, 220, 0.95) 100%)',
        '.chart-card': theme === 'light' ? '#ffffff' : 'white',
        '.activity-card': theme === 'light' ? '#ffffff' : 'white',
        '.quick-actions': theme === 'light' ? '#ffffff' : 'white',
        '.metric-ring': theme === 'light' ? 
            'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)' : 
            'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
        '.contact-gauge, .contact-methods-visual, .contact-timeline': theme === 'light' ? '#ffffff' : '#fff',
        '.role-card': theme === 'light' ? '#ffffff' : '#fff',
        '.user-list': theme === 'light' ? '#ffffff' : '#fff',
        '.permissions-section': theme === 'light' ? '#ffffff' : '#fff'
    };
    
    // Apply styles to all matching elements
    Object.keys(elements).forEach(selector => {
        const elementList = document.querySelectorAll(selector);
        elementList.forEach(element => {
            if (selector.includes('background') || selector.includes('gradient')) {
                element.style.background = elements[selector];
            } else {
                element.style.backgroundColor = elements[selector];
            }
        });
    });
}

// Initialize theme on page load - Global
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    
    // Apply theme globally
    applyTheme(savedTheme);
    
    // Update button text and icon
    const themeBtn = document.querySelector('.theme-btn span');
    const themeIcon = document.querySelector('.theme-btn .nav-icon');
    
    if (themeBtn) {
        themeBtn.textContent = savedTheme === 'dark' ? 'Light Theme' : 'Dark Theme';
    }
    
    if (themeIcon) {
        themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    }
});

// Apply theme when navigating between pages
window.addEventListener('load', function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (document.body.getAttribute('data-theme') !== savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
        applyTheme(savedTheme);
    }
});