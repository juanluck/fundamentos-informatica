function varargout = patata_adivina(accion, varargin)
% PATATA_ADIVINA  Globo con cuenta atras para un juego por consola.
%
% Uso desde el programa del estudiante:
%   patata_adivina('iniciar');                     % Abre la ventana (50-70 s)
%   n = patata_adivina('leer', 'Tu numero: ');     % Se escribe EN LA CONSOLA
%   if isnan(n), return; end                     % Explotó antes de responder
%   if n == numSecreto
%       patata_adivina('acierto');                 % Muestra "¡Has acertado!"
%   end
%
%   patata_adivina('iniciar', 8);  % Solo para pruebas: 8 segundos
%   patata_adivina('cerrar');     % Cierra la interfaz y libera recursos
%
% IMPORTANTE: sustituir input(...) por patata_adivina('leer', ...).
% La funcion input() convencional bloquea la ejecucion en GNU Octave;
% no permitiria actualizar el globo ni terminar a tiempo si nadie responde.
%
% Sin toolboxes. En GNU Octave, usar ventana GUI y escribir en su terminal.
% En MATLAB se usa un timer; en Octave, kbhit(1) + drawnow/pause.

    persistent juego
    if isempty(juego)
        juego = struct('activo', false, 'estado', 'cerrado', ...
                       'fig', [], 'reloj', []);
    end
    if nargin == 0
        accion = 'iniciar';
    end
    if ~ischar(accion)
        error('La primera entrada debe ser: iniciar, leer, acierto o cerrar.');
    end

    switch lower(strtrim(accion))
        case 'iniciar'
            duracion = [];
            if ~isempty(varargin)
                duracion = varargin{1};
                if ~isnumeric(duracion) || ~isscalar(duracion) || ...
                   ~isreal(duracion) || ~isfinite(duracion) || duracion <= 0
                    error('La duracion de prueba debe ser un numero positivo.');
                end
            end
            juego = limpiar_juego(juego);
            juego = crear_juego(duracion);
            % Almacenar el estado antes de iniciar callbacks del timer.
            juego.inicio = tic;
            if ~es_octave()
                try
                    juego.reloj = timer('ExecutionMode', 'fixedSpacing', ...
                        'Period', 0.06, 'BusyMode', 'drop', ...
                        'TimerFcn', @(~,~)patata_adivina('actualizar'));
                    start(juego.reloj);
                catch err
                    juego = limpiar_juego(juego);
                    error('No se pudo iniciar el temporizador MATLAB: %s', err.message);
                end
            end
            fprintf('\n¡La patata caliente ya esta en marcha!\n');
            fprintf('Escribe las respuestas en la ventana de comandos.\n');

        case 'leer'
            % La primera llamada tambien puede arrancar el globo.
            if strcmp(juego.estado, 'cerrado') || ~figura_valida(juego.fig)
                patata_adivina('iniciar');
            end
            patata_adivina('actualizar');
            if ~juego.activo
                numero = NaN;
            else
                mensaje = 'Introduce un numero (0 a 100): ';
                if ~isempty(varargin)
                    mensaje = varargin{1};
                end
                if ~ischar(mensaje)
                    error('El mensaje de entrada debe ser un texto.');
                end
                if es_octave()
                    numero = lectura_octave(mensaje);
                else
                    numero = lectura_matlab(mensaje);
                end
            end
            if nargout > 0
                varargout{1} = numero;
            end

        case 'acierto'
            patata_adivina('actualizar');
            acertado = juego.activo && figura_valida(juego.fig);
            if acertado
                juego.activo = false;
                juego.estado = 'ganado';
                parar_reloj(juego.reloj);
                set(juego.rotulo, 'String', '¡HAS ACERTADO!', ...
                    'ForegroundColor', juego.verde);
                set(juego.pista, 'String', '¡Enhorabuena! Has salvado el globo.', ...
                    'ForegroundColor', juego.verde);
                set(juego.signo, 'String', 'OK', ...
                    'Color', juego.blanco);
                set(juego.presion, 'String', 'OBJETIVO CONSEGUIDO', ...
                    'ForegroundColor', juego.verde);
                drawnow();
                fprintf('\n¡Has acertado!\n');
            end
            if nargout > 0
                varargout{1} = acertado;
            end

        case 'actualizar'
            if juego.activo
                if ~figura_valida(juego.fig)
                    juego.activo = false;
                    juego.estado = 'cerrado';
                    parar_reloj(juego.reloj);
                else
                    transcurrido = toc(juego.inicio);
                    if transcurrido >= juego.duracion
                        % Marcar terminado ANTES de dibujar y procesar eventos.
                        juego.activo = false;
                        juego.estado = 'explotado';
                        parar_reloj(juego.reloj);
                        dibujar_explosion(juego);
                        fprintf('\n\n¡BOOM! Se ha acabado el tiempo.\n');
                        try
                            beep;
                        catch
                        end
                    else
                        dibujar_globo(juego, transcurrido / juego.duracion);
                    end
                end
            end

        case 'activo'
            if nargout > 0
                varargout{1} = juego.activo && figura_valida(juego.fig);
            end

        case 'cerrar'
            juego = limpiar_juego(juego);

        otherwise
            error('Accion desconocida. Usa iniciar, leer, acierto o cerrar.');
    end
end

% ======================================================================
% Funciones auxiliares; no es necesario que los alumnos las modifiquen.
% ======================================================================
function tf = es_octave()
    tf = exist('OCTAVE_VERSION', 'builtin') ~= 0;
end

function tf = figura_valida(fig)
    tf = ~isempty(fig) && ishandle(fig);
end

function j = crear_juego(duracion)
    j = struct();
    j.activo = true;
    j.estado = 'jugando';
    j.reloj = [];
    if isempty(duracion)
        j.duracion = randi([50, 70]);
    else
        j.duracion = duracion;
    end

    j.fondo   = [0.075 0.105 0.17];
    j.blanco  = [0.96 0.97 0.99];
    j.suave   = [0.73 0.79 0.87];
    j.amarillo = [1.00 0.84 0.32];
    j.verde   = [0.43 0.91 0.60];
    j.rojo    = [0.99 0.30 0.34];

    j.fig = figure('Name', 'PATATA CALIENTE - Adivina el numero', ...
        'NumberTitle', 'off', 'MenuBar', 'none', 'ToolBar', 'none', ...
        'Resize', 'off', 'Color', j.fondo, 'Position', [170 110 760 530], ...
        'CloseRequestFcn', @(~,~)patata_adivina('cerrar'));

    uicontrol('Parent', j.fig, 'Style', 'text', ...
        'Units', 'normalized', 'Position', [0.07 0.89 0.86 0.083], ...
        'BackgroundColor', j.fondo, 'ForegroundColor', j.blanco, ...
        'FontSize', 25, 'FontWeight', 'bold', 'String', 'PATATA CALIENTE');
    uicontrol('Parent', j.fig, 'Style', 'text', ...
        'Units', 'normalized', 'Position', [0.06 0.82 0.88 0.055], ...
        'BackgroundColor', j.fondo, 'ForegroundColor', j.suave, ...
        'FontSize', 12, 'String', 'Adivina el numero secreto entre 0 y 100');

    j.rotulo = uicontrol('Parent', j.fig, 'Style', 'text', ...
        'Units', 'normalized', 'Position', [0.05 0.725 0.90 0.075], ...
        'BackgroundColor', j.fondo, 'ForegroundColor', j.amarillo, ...
        'FontSize', 19, 'FontWeight', 'bold', 'String', '¡CORRE, QUE SE HINCHA!');

    j.ax = axes('Parent', j.fig, 'Units', 'normalized', ...
        'Position', [0.095 0.16 0.52 0.56], 'Color', j.fondo);
    axis(j.ax, [-1.5 1.5 -1.4 1.5]);
    axis(j.ax, 'equal');
    axis(j.ax, 'off');
    hold(j.ax, 'on');

    j.angulo = linspace(0, 2*pi, 150);
    j.cuerda = line('Parent', j.ax, 'XData', [0 0], ...
        'YData', [-0.5 -1.3], 'Color', j.suave, 'LineWidth', 2);
    j.globo = patch('Parent', j.ax, 'XData', 0.45*cos(j.angulo), ...
        'YData', 0.15 + 0.45*sin(j.angulo), ...
        'FaceColor', [0.98 0.47 0.20], ...
        'EdgeColor', [0.75 0.21 0.16], 'LineWidth', 2);
    j.brillo = patch('Parent', j.ax, 'XData', -0.1 + 0.07*cos(j.angulo), ...
        'YData', 0.36 + 0.12*sin(j.angulo), ...
        'FaceColor', [1 0.85 0.72], 'EdgeColor', 'none');
    j.signo = text(0, 0.15, '?', 'Parent', j.ax, ...
        'Color', j.blanco, 'FontSize', 44, 'FontWeight', 'bold', ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');

    j.rayos = cell(1, 14);
    for k = 1:14
        j.rayos{k} = line('Parent', j.ax, 'XData', [0 0], ...
            'YData', [0 0], 'Color', j.amarillo, ...
            'LineWidth', 3.5, 'Visible', 'off');
    end
    j.boom = text(0, 0.15, '¡BOOM!', 'Parent', j.ax, ...
        'Color', j.amarillo, 'FontSize', 38, 'FontWeight', 'bold', ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
        'Visible', 'off');

    j.presion = uicontrol('Parent', j.fig, 'Style', 'text', ...
        'Units', 'normalized', 'Position', [0.62 0.58 0.33 0.075], ...
        'BackgroundColor', j.fondo, 'ForegroundColor', j.amarillo, ...
        'FontSize', 17, 'FontWeight', 'bold', 'String', 'PRESION: 0 %');

    j.pista = uicontrol('Parent', j.fig, 'Style', 'text', ...
        'Units', 'normalized', 'Position', [0.61 0.36 0.35 0.19], ...
        'BackgroundColor', j.fondo, 'ForegroundColor', j.blanco, ...
        'FontSize', 15, 'FontWeight', 'bold', ...
        'String', {'Introduce tus numeros'; 'en la CONSOLA'; 'de MATLAB / Octave'});

    uicontrol('Parent', j.fig, 'Style', 'text', ...
        'Units', 'normalized', 'Position', [0.05 0.045 0.90 0.065], ...
        'BackgroundColor', j.fondo, 'ForegroundColor', j.suave, ...
        'FontSize', 10, 'String', ...
        'El reloj no se detiene entre intentos. ¡No sabes cuando explotara!');

    dibujar_globo(j, 0);
    drawnow();
end

function dibujar_globo(j, fraccion)
    if ~figura_valida(j.fig)
        return;
    end
    fraccion = min(1, max(0, fraccion));
    r = 0.46 + 0.60*(fraccion^1.10);
    y0 = 0.15;
    set(j.globo, 'XData', r*cos(j.angulo), ...
        'YData', y0 + r*sin(j.angulo), ...
        'FaceColor', (1-fraccion)*[0.98 0.47 0.20] + ...
                     fraccion*[0.86 0.12 0.20]);
    set(j.brillo, 'XData', -0.33*r + 0.12*r*cos(j.angulo), ...
        'YData', y0 + 0.38*r + 0.20*r*sin(j.angulo));
    set(j.cuerda, 'XData', [0 0.03 -0.03 0], ...
        'YData', [y0-r y0-r-0.20 -1.17 -1.34]);
    set(j.signo, 'FontSize', 40 + round(fraccion*18));
    set(j.presion, 'String', sprintf('PRESION: %d %%', round(fraccion*100)));
    if fraccion > 0.83
        set(j.presion, 'ForegroundColor', j.rojo);
    end
    drawnow();
end

function dibujar_explosion(j)
    if ~figura_valida(j.fig)
        return;
    end
    set(j.globo, 'Visible', 'off');
    set(j.brillo, 'Visible', 'off');
    set(j.cuerda, 'Visible', 'off');
    set(j.signo, 'Visible', 'off');
    for k = 1:numel(j.rayos)
        a = 2*pi*(k-1)/numel(j.rayos);
        set(j.rayos{k}, 'XData', [0.55*cos(a), 1.25*cos(a)], ...
            'YData', [0.15+0.55*sin(a), 0.15+1.25*sin(a)], ...
            'Visible', 'on');
    end
    set(j.boom, 'Visible', 'on');
    set(j.rotulo, 'String', '¡SE ACABO EL TIEMPO!', ...
        'ForegroundColor', j.rojo);
    set(j.pista, 'String', {'No has conseguido'; 'adivinarlo a tiempo.'}, ...
        'ForegroundColor', j.rojo);
    set(j.presion, 'String', '¡EXPLOSION!', 'ForegroundColor', j.rojo);
    drawnow();
end

function parar_reloj(t)
    if ~isempty(t)
        try
            stop(t);
        catch
        end
    end
end

function j = limpiar_juego(j)
    if isfield(j, 'reloj') && ~isempty(j.reloj)
        parar_reloj(j.reloj);
        try
            delete(j.reloj);
        catch
        end
    end
    if isfield(j, 'fig') && figura_valida(j.fig)
        try
            delete(j.fig);
        catch
        end
    end
    j = struct('activo', false, 'estado', 'cerrado', ...
               'fig', [], 'reloj', []);
end

function numero = lectura_octave(mensaje)
    % kbhit(1) consulta el teclado SIN esperar. Asi se sigue dibujando
    % el globo y se puede terminar el juego aunque no se pulse INTRO.
    fprintf('%s', mensaje);
    fflush(stdout);
    cadena = '';
    numero = NaN;
    while true
        patata_adivina('actualizar');
        if ~patata_adivina_activo()
            fprintf('\n');
            return;
        end
        tecla = kbhit(1);
        if isempty(tecla)
            pause(0.04);
            continue;
        end
        codigo = double(tecla(1));
        if codigo == 13 || codigo == 10   % INTRO
            fprintf('\n');
            numero = str2double(strtrim(cadena));
            if numero_valido(numero)
                patata_adivina('actualizar');
                if ~patata_adivina_activo()
                    numero = NaN;
                end
                return;
            end
            fprintf('Escribe un entero entre 0 y 100.\n%s', mensaje);
            cadena = '';
        elseif codigo == 8 || codigo == 127  % RETROCESO
            if ~isempty(cadena)
                cadena = cadena(1:end-1);
                fprintf('\b \b');
            end
        elseif ~isempty(regexp(tecla, '^[0-9]$', 'once')) && length(cadena) < 3
            cadena = [cadena tecla]; %#ok<AGROW>
            fprintf('%s', tecla);
        end
        fflush(stdout);
    end
end

function tf = patata_adivina_activo()
    % Consulta segura del estado, sin exponer la variable persistente.
    tf = patata_adivina('activo');
end

function numero = lectura_matlab(mensaje)
    % MATLAB procesa callbacks de timer mientras input espera una linea.
    % En algunas instalaciones, si explota antes de INTRO, la GUI muestra
    % la explosion al instante pero input puede seguir esperando INTRO.
    numero = NaN;
    while patata_adivina_activo()
        cadena = input(mensaje, 's');
        patata_adivina('actualizar');
        if ~patata_adivina_activo()
            return;
        end
        numero = str2double(strtrim(cadena));
        if numero_valido(numero)
            return;
        end
        fprintf('Escribe un entero entre 0 y 100.\n');
    end
end

function tf = numero_valido(n)
    tf = isnumeric(n) && isscalar(n) && isreal(n) && ...
         isfinite(n) && n == fix(n) && n >= 0 && n <= 100;
end