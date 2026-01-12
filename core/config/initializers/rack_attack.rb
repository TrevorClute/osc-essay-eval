class Rack::Attack
  Rack::Attack.cache.store = ActiveSupport::Cache::MemoryStore.new 

  throttle('essays/ip', limit: 10, period: 1.minutes) do |req|
    if req.path == '/essays' && req.post?
      req.ip
    end
  end
end
