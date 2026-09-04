/* ============================================================
   AfricaStudy Connect — interactions du site
   ============================================================ */
(function () {
    'use strict';

    /* ---------- Menu mobile ---------- */
    var menuToggle = document.getElementById('menuToggle');
    var navMenu = document.getElementById('navMenu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function () {
            var open = navMenu.classList.toggle('active');
            menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });

        document.addEventListener('click', function (e) {
            if (!e.target.closest('header') && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    /* ---------- Défilement fluide vers les ancres ---------- */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var targetId = this.getAttribute('href');
            if (!targetId || targetId === '#') return;
            var target = document.querySelector(targetId);
            if (!target) return;
            e.preventDefault();
            if (navMenu) {
                navMenu.classList.remove('active');
                if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
            }
            target.scrollIntoView({ behavior: 'smooth' });
            history.replaceState(null, '', targetId);
        });
    });

    /* ---------- Bouton « retour en haut » ---------- */
    var backToTop = document.getElementById('backToTop');
    if (backToTop) {
        var toggleBackToTop = function () {
            backToTop.classList.toggle('visible', window.scrollY > 600);
        };
        window.addEventListener('scroll', toggleBackToTop, { passive: true });
        toggleBackToTop();
        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* ---------- Compteurs animés au scroll ---------- */
    var counters = document.querySelectorAll('[data-count]');
    if (counters.length && 'IntersectionObserver' in window) {
        var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        var format = function (n) {
            return n.toLocaleString('fr-FR').replace(/ | /g, ' ');
        };

        var animate = function (el) {
            var target = parseInt(el.dataset.count, 10);
            var prefix = el.dataset.prefix || '';
            var suffix = el.dataset.suffix || '';
            if (isNaN(target)) return;

            if (reduceMotion) {
                el.textContent = prefix + format(target) + suffix;
                return;
            }

            var duration = 1400;
            var start = null;
            var step = function (ts) {
                if (start === null) start = ts;
                var progress = Math.min((ts - start) / duration, 1);
                // easing out cubic
                var eased = 1 - Math.pow(1 - progress, 3);
                el.textContent = prefix + format(Math.round(target * eased)) + suffix;
                if (progress < 1) requestAnimationFrame(step);
            };
            requestAnimationFrame(step);
        };

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animate(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.4 });

        counters.forEach(function (el) { observer.observe(el); });
    }

    /* ---------- Notifications ---------- */
    var notifTimer = null;
    function notify(message, type) {
        var n = document.getElementById('notif');
        if (!n) {
            n = document.createElement('div');
            n.id = 'notif';
            n.setAttribute('role', 'status');
            n.setAttribute('aria-live', 'polite');
            document.body.appendChild(n);
        }
        n.className = 'notif ' + (type === 'success' ? 'success' : 'error');
        n.textContent = message;
        // force reflow pour rejouer la transition
        void n.offsetWidth;
        n.classList.add('show');
        clearTimeout(notifTimer);
        notifTimer = setTimeout(function () { n.classList.remove('show'); }, 6000);
    }

    /* ---------- Formulaire de contact ---------- */
    var form = document.getElementById('leadForm');
    if (!form) return;

    var MAX_FILES = 3;
    var MAX_SIZE = 5 * 1024 * 1024;
    var ALLOWED = ['application/pdf', 'image/jpeg', 'image/png'];

    var fileInput = document.getElementById('documents');
    var fileDrop = document.getElementById('fileDrop');
    var fileListEl = document.getElementById('fileList');
    var selectedFiles = [];

    function humanSize(bytes) {
        if (bytes < 1024) return bytes + ' o';
        if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + ' Ko';
        return (bytes / (1024 * 1024)).toFixed(1).replace('.', ',') + ' Mo';
    }

    function renderFiles() {
        if (!fileListEl) return;
        fileListEl.innerHTML = '';
        selectedFiles.forEach(function (file, index) {
            var li = document.createElement('li');
            var label = document.createElement('span');
            label.textContent = file.name + ' — ' + humanSize(file.size);
            var remove = document.createElement('button');
            remove.type = 'button';
            remove.setAttribute('aria-label', 'Retirer ' + file.name);
            remove.innerHTML = '<i class="fas fa-xmark" aria-hidden="true"></i>';
            remove.addEventListener('click', function () {
                selectedFiles.splice(index, 1);
                renderFiles();
            });
            li.appendChild(label);
            li.appendChild(remove);
            fileListEl.appendChild(li);
        });
    }

    function addFiles(files) {
        var errors = [];
        Array.prototype.forEach.call(files, function (file) {
            if (selectedFiles.length >= MAX_FILES) {
                errors.push('3 fichiers maximum.');
                return;
            }
            if (ALLOWED.indexOf(file.type) === -1) {
                errors.push(file.name + ' : format non accepté (PDF, JPG ou PNG uniquement).');
                return;
            }
            if (file.size > MAX_SIZE) {
                errors.push(file.name + ' : dépasse 5 Mo.');
                return;
            }
            selectedFiles.push(file);
        });
        renderFiles();
        setError('documents', errors.length ? errors[0] : '');
    }

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            addFiles(this.files);
            this.value = '';
        });
    }

    if (fileDrop) {
        ['dragenter', 'dragover'].forEach(function (evt) {
            fileDrop.addEventListener(evt, function (e) {
                e.preventDefault();
                fileDrop.classList.add('dragover');
            });
        });
        ['dragleave', 'drop'].forEach(function (evt) {
            fileDrop.addEventListener(evt, function (e) {
                e.preventDefault();
                fileDrop.classList.remove('dragover');
            });
        });
        fileDrop.addEventListener('drop', function (e) {
            if (e.dataTransfer && e.dataTransfer.files) addFiles(e.dataTransfer.files);
        });
    }

    /* ---------- Validation en temps réel ---------- */
    function setError(field, message) {
        var errEl = document.getElementById('err-' + field);
        var input = document.getElementById(field === 'documents' ? 'documents' : field);
        if (errEl) {
            errEl.textContent = message || '';
            errEl.classList.toggle('show', !!message);
        }
        if (input && input.classList.contains('form-control')) {
            input.classList.toggle('invalid', !!message);
            input.setAttribute('aria-invalid', message ? 'true' : 'false');
        }
    }

    var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    function validateField(id) {
        var el = document.getElementById(id);
        if (!el) return true;
        var value = (el.value || '').trim();

        switch (id) {
            case 'fullname':
                if (value.length < 2) { setError('fullname', 'Indiquez votre nom et votre prénom.'); return false; }
                break;
            case 'email':
                if (!EMAIL_RE.test(value)) { setError('email', 'Cette adresse e-mail semble incorrecte.'); return false; }
                break;
            case 'phone':
                var digits = value.replace(/\D/g, '');
                if (digits.length < 6) { setError('phone', 'Numéro trop court — indiquez votre numéro WhatsApp complet.'); return false; }
                if (digits.length > 15) { setError('phone', 'Numéro trop long — vérifiez votre saisie.'); return false; }
                break;
            case 'originCountry':
                if (!value) { setError('originCountry', 'Sélectionnez votre pays de résidence.'); return false; }
                break;
            case 'destinationCountry':
                if (!value) { setError('destinationCountry', 'Sélectionnez la destination souhaitée.'); return false; }
                break;
            case 'studyLevel':
                if (!value) { setError('studyLevel', 'Sélectionnez votre niveau d\'études.'); return false; }
                break;
            case 'consent':
                if (!el.checked) { setError('consent', 'Votre accord est nécessaire pour traiter la demande.'); return false; }
                break;
        }
        setError(id, '');
        return true;
    }

    var VALIDATED = ['fullname', 'email', 'phone', 'originCountry', 'destinationCountry', 'studyLevel', 'consent'];

    VALIDATED.forEach(function (id) {
        var el = document.getElementById(id);
        if (!el) return;
        var evt = (el.tagName === 'SELECT' || el.type === 'checkbox') ? 'change' : 'blur';
        el.addEventListener(evt, function () { validateField(id); });
        el.addEventListener('input', function () {
            // on efface l'erreur dès que l'utilisateur corrige
            var errEl = document.getElementById('err-' + id);
            if (errEl && errEl.classList.contains('show')) validateField(id);
        });
    });

    /* ---------- Soumission ---------- */
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        var firstInvalid = null;
        VALIDATED.forEach(function (id) {
            if (!validateField(id) && !firstInvalid) firstInvalid = document.getElementById(id);
        });
        if (firstInvalid) {
            firstInvalid.focus();
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            notify('Certains champs demandent une correction.', 'error');
            return;
        }

        var btn = document.getElementById('submitBtn');
        var originalHtml = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-circle-notch fa-spin" aria-hidden="true"></i> Envoi en cours…';

        var code = document.getElementById('phoneCode');
        var codeValue = code && code.value !== 'autre' ? code.value + ' ' : '';

        var payload = {
            name: document.getElementById('fullname').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: (codeValue + document.getElementById('phone').value.trim()).trim(),
            country: document.getElementById('originCountry').value,
            destination: document.getElementById('destinationCountry').value,
            level: document.getElementById('studyLevel').value,
            formula: document.getElementById('formula').value || 'À déterminer avec le conseiller',
            postbac: document.getElementById('postbacOption').checked,
            message: document.getElementById('message').value.trim(),
            consent: true
        };

        fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(function (res) {
                // L'API peut renvoyer une page d'erreur HTML (502, 404, maintenance) :
                // on ne laisse jamais l'erreur de parsing remonter jusqu'à l'utilisateur.
                return res.text().then(function (text) {
                    var data = null;
                    try { data = JSON.parse(text); } catch (e) { /* réponse non JSON */ }
                    return { ok: res.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok || !result.data) {
                    throw new Error(
                        result.data && result.data.error
                            ? result.data.error
                            : 'Envoi impossible pour le moment. Réessayez, ou écrivez-nous sur WhatsApp.'
                    );
                }
                return uploadDocuments(payload.email);
            })
            .then(function (uploadWarning) {
                form.reset();
                selectedFiles = [];
                renderFiles();
                VALIDATED.forEach(function (id) { setError(id, ''); });
                notify(
                    uploadWarning
                        ? 'Demande enregistrée. ' + uploadWarning + ' Un conseiller vous contacte sous 24 h.'
                        : 'Merci ! Votre demande est enregistrée. Un conseiller vous contacte sous 24 h.',
                    'success'
                );
                if (window.plausible) window.plausible('Lead');
            })
            .catch(function (err) {
                notify(err.message || 'Erreur de connexion. Réessayez ou écrivez-nous sur WhatsApp.', 'error');
            })
            .finally(function () {
                btn.disabled = false;
                btn.innerHTML = originalHtml;
            });
    });

    function uploadDocuments(email) {
        if (!selectedFiles.length) return Promise.resolve('');

        var uploads = selectedFiles.map(function (file) {
            var fd = new FormData();
            fd.append('file', file);
            fd.append('email', email);
            return fetch('/api/upload', { method: 'POST', body: fd })
                .then(function (res) { return res.ok; })
                .catch(function () { return false; });
        });

        return Promise.all(uploads).then(function (results) {
            var failed = results.filter(function (ok) { return !ok; }).length;
            if (!failed) return '';
            return failed === results.length
                ? 'L\'envoi des documents a échoué — vous pourrez les transmettre par e-mail.'
                : failed + ' document(s) n\'ont pas pu être envoyés.';
        });
    }
})();
